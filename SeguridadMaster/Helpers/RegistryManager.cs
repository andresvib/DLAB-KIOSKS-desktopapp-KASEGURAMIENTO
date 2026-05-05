using Microsoft.Win32;
using System;
using System.Diagnostics;

namespace SeguridadMaster.Helpers
{
    public static class RegistryManager
    {
        public static void ApplySecurityPolicies()
        {
            try
            {
                Debug.WriteLine("=== INICIANDO BLOQUEO SEGURO (SOLO ALMACENAMIENTO) ===");

                // CAPA 1: Denegar acceso lógico (No apaga el hardware, solo prohíbe abrir archivos)
                ApplyUsbGpoPolicy();

                // CAPA 2: Deshabilitar el Driver USBSTOR (El estándar para memorias USB)
                // Esto NO afecta a pantallas táctiles, teclados o scanners (clase HID)
                DisableUsbStorService();

                // CAPA 3: Ejecutar actualización de políticas
                ForcePolicyUpdate();

                Debug.WriteLine("=== BLOQUEO APLICADO: PERIFÉRICOS PROTEGIDOS ===");
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error crítico: {ex.Message}");
                throw;
            }
        }

        private static void ApplyUsbGpoPolicy()
        {
            try
            {
                string policyPath = @"SOFTWARE\Policies\Microsoft\Windows\RemovableStorageDevices";
                using (RegistryKey key = Registry.LocalMachine.CreateSubKey(policyPath, true))
                {
                    // Bloquea lectura, escritura y ejecución en discos extraíbles
                    key.SetValue("Deny_All", 1, RegistryValueKind.DWord);
                }
            }
            catch (Exception ex) { Debug.WriteLine($"Error GPO: {ex.Message}"); }
        }

        private static void DisableUsbStorService()
        {
            try
            {
                // El valor '4' deshabilita el driver de almacenamiento masivo únicamente.
                string usbStorPath = @"SYSTEM\CurrentControlSet\Services\USBSTOR";
                using (RegistryKey key = Registry.LocalMachine.OpenSubKey(usbStorPath, true))
                {
                    if (key != null)
                    {
                        key.SetValue("Start", 4, RegistryValueKind.DWord);
                    }
                }

                // Forzamos la detención del servicio de almacenamiento si ya hay una USB puesta
                ExecuteCommand("sc.exe", "stop USBSTOR", true);
            }
            catch (Exception ex) { Debug.WriteLine($"Error USBSTOR: {ex.Message}"); }
        }

        public static void RestoreDefaults()
        {
            try
            {
                Debug.WriteLine("=== RESTAURANDO SISTEMA TOTAL ===");

                // 1. Limpiar TODAS las políticas de restricción de raíz
                using (RegistryKey key = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Policies\Microsoft\Windows", true))
                {
                    key?.DeleteSubKeyTree("RemovableStorageDevices", false);
                    key?.DeleteSubKeyTree("DeviceInstall", false); // Limpia rastros de bloqueos anteriores
                }

                // 2. Rehabilitar el servicio USBSTOR (Valor 3 = Manual/Demanda)
                Registry.SetValue(@"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBSTOR", "Start", 3, RegistryValueKind.DWord);

                // 3. COMANDO DE RESCATE: Despertar cualquier dispositivo USB que haya quedado deshabilitado por error
                ExecuteCommand("powershell.exe", "Get-PnpDevice -Class USB -Status Disabled | Enable-PnpDevice -Confirm:$false", false);

                // 4. Actualizar comandos de sistema
                ExecuteCommand("sc.exe", "config USBSTOR start= demand", true);
                ExecuteCommand("sc.exe", "start USBSTOR", false);
                ExecuteCommand("gpupdate.exe", "/force", false);

                Debug.WriteLine("=== SISTEMA RESTAURADO CORRECTAMENTE ===");
            }
            catch (Exception ex) { Debug.WriteLine($"Error en restauración: {ex.Message}"); }
        }

        private static void ForcePolicyUpdate()
        {
            ExecuteCommand("gpupdate.exe", "/force", false);
        }

        private static void ExecuteCommand(string fileName, string arguments, bool waitForExit)
        {
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = fileName,
                    Arguments = arguments,
                    WindowStyle = ProcessWindowStyle.Hidden,
                    CreateNoWindow = true,
                    UseShellExecute = false
                };

                Process process = Process.Start(psi);
                if (waitForExit) process?.WaitForExit(5000);
            }
            catch (Exception ex) { Debug.WriteLine($"Error ejecutando {fileName}: {ex.Message}"); }
        }
    }
}