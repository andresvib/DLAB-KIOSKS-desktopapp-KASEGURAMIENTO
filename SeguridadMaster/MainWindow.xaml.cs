using System;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Linq;
using System.Security.Principal;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Win32.TaskScheduler;
using SeguridadMaster.Helpers;
using SeguridadMaster.Services;
using CSharpTask = System.Threading.Tasks.Task;
using WinTask = Microsoft.Win32.TaskScheduler;

namespace SeguridadMaster
{
    public partial class MainWindow : Window
    {
        private KeyboardHook _hook;
        private Process? _targetApp;

        // Mantenemos la lista interna por si los servicios de red la necesitan, 
        // pero ya no está vinculada a la interfaz gráfica.
        private ObservableCollection<string> _whiteListIps = new ObservableCollection<string>();

        private bool _isUsbBlocked = false;

        public MainWindow()
        {
            // 1. VALIDACIÓN DE PRIVILEGIOS
            if (!IsRunAsAdmin())
            {
                ElevateToAdmin();
                return;
            }

            InitializeComponent();

            // 2. CONFIGURAR INICIO AUTOMÁTICO
            RegistrarTareaProgramada();

            // 3. INICIALIZAR COMPONENTES
            _hook = new KeyboardHook();
            _hook.OnUnlockTriggered += RestorationAndExit;

            // IP local por defecto (ya no se muestra en ListBox)
            _whiteListIps.Add("127.0.0.1");

            // 4. DISPARADOR AUTOMÁTICO
            this.Loaded += async (s, e) =>
            {
                await CSharpTask.Delay(2000);
                OnStartProtection(null, null);
            };
        }

        #region Gestión de Privilegios y Tareas

        private bool IsRunAsAdmin()
        {
            var identity = WindowsIdentity.GetCurrent();
            var principal = new WindowsPrincipal(identity);
            return principal.IsInRole(WindowsBuiltInRole.Administrator);
        }

        private void ElevateToAdmin()
        {
            ProcessStartInfo proc = new ProcessStartInfo();
            proc.UseShellExecute = true;
            proc.WorkingDirectory = Environment.CurrentDirectory;
            proc.FileName = Process.GetCurrentProcess().MainModule.FileName;
            proc.Verb = "runas";

            try
            {
                Process.Start(proc);
                Application.Current.Shutdown();
            }
            catch (Exception)
            {
                MessageBox.Show("Esta aplicación requiere permisos de administrador.");
                Application.Current.Shutdown();
            }
        }

        private void RegistrarTareaProgramada()
        {
            try
            {
                using (WinTask.TaskService ts = new WinTask.TaskService())
                {
                    string taskName = "SeguridadMaster_AutoStart";
                    string exePath = Process.GetCurrentProcess().MainModule.FileName;

                    if (ts.GetTask(taskName) != null) return;

                    WinTask.TaskDefinition td = ts.NewTask();
                    td.RegistrationInfo.Description = "Inicia el escudo de seguridad de SeguridadMaster.";
                    td.Triggers.Add(new WinTask.LogonTrigger());
                    td.Actions.Add(new WinTask.ExecAction(exePath, null, null));
                    td.Principal.RunLevel = WinTask.TaskRunLevel.Highest;
                    td.Settings.DisallowStartIfOnBatteries = false;
                    td.Settings.StopIfGoingOnBatteries = false;
                    td.Settings.ExecutionTimeLimit = TimeSpan.Zero;

                    ts.RootFolder.RegisterTaskDefinition(taskName, td);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine("Error al registrar la tarea: " + ex.Message);
            }
        }

        #endregion

        #region Lógica de Protección y USB

        private async void OnUsbControl_Click(object sender, RoutedEventArgs e)
        {
            btnUsbControl.IsEnabled = false;
            try
            {
                if (!_isUsbBlocked)
                {
                    btnUsbControl.Content = "BLOQUEANDO...";
                    await CSharpTask.Run(() => RegistryManager.ApplySecurityPolicies());
                    _isUsbBlocked = true;
                    btnUsbControl.Content = "USB: BLOQUEADO";
                    btnUsbControl.Background = System.Windows.Media.Brushes.Crimson;
                }
                else
                {
                    btnUsbControl.Content = "HABILITANDO...";
                    await CSharpTask.Run(() => RegistryManager.RestoreDefaults());
                    _isUsbBlocked = false;
                    btnUsbControl.Content = "USB: PERMITIDO";
                    btnUsbControl.Background = System.Windows.Media.Brushes.ForestGreen;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error al gestionar USB: {ex.Message}");
            }
            finally
            {
                btnUsbControl.IsEnabled = true;
            }
        }

        private async void OnStartProtection(object sender, RoutedEventArgs e)
        {
            if (btnIniciar.IsEnabled == false && sender != null) return;

            btnIniciar.IsEnabled = false;
            btnIniciar.Content = "PROTEGIENDO...";

            try
            {
                // 1. Registro y USB
                RegistryManager.ApplySecurityPolicies();
                ledRegistry.Tag = "Active";
                pgBar.Value = 20;

                _isUsbBlocked = true;
                btnUsbControl.Content = "USB: BLOQUEADO";
                btnUsbControl.Background = System.Windows.Media.Brushes.Crimson;

                await CSharpTask.Delay(500);

                // 2. Network (Usa la lista interna de IPs)
                string[] ips = _whiteListIps.ToArray();
                NetworkService.ConfigureRestrictedRDP(ips);
                NetworkService.BlockFTP();
                ledFirewall.Tag = "Active";
                pgBar.Value = 50;
                await CSharpTask.Delay(500);

                // 3. WiFi
                NetworkService.DisableWiFi();
                ledWifi.Tag = "Active";
                pgBar.Value = 70;
                await CSharpTask.Delay(500);

                // 4. Hook
                _hook.Start();
                ledHook.Tag = "Active";
                pgBar.Value = 90;
                await CSharpTask.Delay(500);

                // 5. App Supervisora
                _targetApp = Process.Start(@"C:\Program Files\Datec\SuperVisor\SuperVisor.WPF.exe");
                // Nota: Asegúrate de tener ledApp definido en el XAML o comenta la línea siguiente:
                // ledApp.Tag = "Active"; 
                pgBar.Value = 100;

                btnIniciar.Content = "ESCUDO ACTIVADO";
                btnIniciar.Background = System.Windows.Media.Brushes.DarkSlateBlue;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
                RestorationAndExit();
            }
        }

        private void RestorationAndExit()
        {
            Dispatcher.Invoke(() => {
                try
                {
                    // 1. SONIDO Y LIBERAR HOOK
                    System.Media.SystemSounds.Exclamation.Play();
                    _hook?.Stop();

                    // 2. MOSTRAR TU VENTANA PERSONALIZADA (XAML)
                    NotificacionDesbloqueo nDialog = new NotificacionDesbloqueo();
                    nDialog.Topmost = true;
                    nDialog.ShowDialog();

                    // 3. CIERRE FORZOSO DEL SUPERVISOR
                    try
                    {
                        if (_targetApp != null && !_targetApp.HasExited) _targetApp.Kill();

                        var procesos = Process.GetProcessesByName("SuperVisor.WPF");
                        foreach (var p in procesos) { p.Kill(); }
                    }
                    catch { /* Ignorar errores de cierre */ }

                    // --- BLOQUE NUEVO: LEVANTAR EL ESCRITORIO (EXPLORER) ---
                    try
                    {
                        // Verificamos si explorer ya está corriendo, si no, lo lanzamos
                        var explorers = Process.GetProcessesByName("explorer");
                        if (explorers.Length == 0)
                        {
                            Process.Start("explorer.exe");
                        }
                    }
                    catch (Exception ex)
                    {
                        Debug.WriteLine("No se pudo iniciar explorer: " + ex.Message);
                    }
                    // -------------------------------------------------------

                    // 4. CERRAR SEGURIDADMASTER
                    Application.Current.Shutdown();
                }
                catch (Exception ex)
                {
                    Debug.WriteLine("Error crítico: " + ex.Message);
                    Application.Current.Shutdown();
                }
            });
        }

        #endregion
    }
}