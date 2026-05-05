using System;
using System.Diagnostics;
using System.Linq;

namespace SeguridadMaster.Services
{
    public static class NetworkService
    {
        // Nombre de la regla unificado para la auditoría
        private const string RDP_RULE_NAME = "SeguridadMaster_RDP_Restricted";
        private const string FTP_RULE_NAME = "SeguridadMaster_Block_FTP";

        public static void ConfigureRestrictedRDP(string[] allowedIPs)
        {
            if (allowedIPs == null || allowedIPs.Length == 0) return;

            string ipList = string.Join(",", allowedIPs);

            // 1. Limpiamos cualquier regla previa
            RunNetsh($"advfirewall firewall delete rule name=\"{RDP_RULE_NAME}\"");

            // 2. Creamos la regla de firewall restrictiva (Entrada)
            string command = $"advfirewall firewall add rule name=\"{RDP_RULE_NAME}\" " +
                             $"dir=in action=allow protocol=TCP localport=3389 " +
                             $"remoteip={ipList} description=\"Acceso RDP limitado por SeguridadMaster\"";

            RunNetsh(command);
        }

        public static void BlockFTP()
        {
            // Limpiar antes de agregar para evitar duplicados
            RunNetsh($"advfirewall firewall delete rule name=\"{FTP_RULE_NAME}\"");

            // Bloqueo de salida puerto 21
            RunNetsh($"advfirewall firewall add rule name=\"{FTP_RULE_NAME}\" dir=out action=block protocol=TCP remoteport=21");
        }

        public static void DisableWiFi()
        {
            // En lugar de usar solo "Wi-Fi", usamos un comando de interfaz más genérico
            // que deshabilita cualquier adaptador que se identifique como inalámbrico
            RunPowerShell("Get-NetAdapter | Where-Object { $_.InterfaceDescription -Match 'Wireless|Wi-Fi' } | Disable-NetAdapter -Confirm:$false");

            // También deshabilitamos el servicio de zona con cobertura inalámbrica (Hotspot)
            RunNetsh("interface set interface name=\"Wi-Fi\" admin=disabled");
        }

        public static void RestoreNetworkDefaults()
        {
            RunNetsh($"advfirewall firewall delete rule name=\"{RDP_RULE_NAME}\"");
            RunNetsh($"advfirewall firewall delete rule name=\"{FTP_RULE_NAME}\"");

            // Re-habilitar adaptadores inalámbricos
            RunPowerShell("Get-NetAdapter | Where-Object { $_.InterfaceDescription -Match 'Wireless|Wi-Fi' } | Enable-NetAdapter -Confirm:$false");
        }

        private static void RunNetsh(string args)
        {
            EjecutarProceso("netsh", args);
        }

        private static void RunPowerShell(string command)
        {
            EjecutarProceso("powershell", $"-Command \"{command}\"");
        }

        private static void EjecutarProceso(string fileName, string args)
        {
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo(fileName, args)
                {
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    WindowStyle = ProcessWindowStyle.Hidden
                };
                Process.Start(psi)?.WaitForExit();
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error ejecutando {fileName}: {ex.Message}");
            }
        }
    }
}