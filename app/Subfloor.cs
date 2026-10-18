// Subfloor desktop app: a native window that shows the synth page from the local web\ folder.
// Built with the C# compiler that ships with Windows (.NET Framework 4.x), see build.ps1.
using System;
using System.Drawing;
using System.IO;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.WinForms;

[assembly: System.Reflection.AssemblyTitle("Subfloor")]
[assembly: System.Reflection.AssemblyProduct("Subfloor")]
[assembly: System.Reflection.AssemblyDescription("Mono sub-bass and bass synth")]
[assembly: System.Reflection.AssemblyVersion("1.2.0.0")]
[assembly: System.Reflection.AssemblyFileVersion("1.2.0.0")]

static class Program
{
    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new MainForm());
    }
}

class MainForm : Form
{
    // A reserved .example host: WebView2 serves it from disk, so nothing ever goes to the network.
    const string Host = "subfloor.example";
    static readonly Color Panel = Color.FromArgb(20, 22, 29);
    readonly WebView2 web;

    public MainForm()
    {
        Text = "Subfloor";
        Icon = Icon.ExtractAssociatedIcon(Application.ExecutablePath);
        BackColor = Panel;
        StartPosition = FormStartPosition.CenterScreen;

        float scale = DeviceDpi / 96f;
        Rectangle area = Screen.FromPoint(Cursor.Position).WorkingArea;
        Size = new Size(Math.Min((int)(1140 * scale), area.Width), Math.Min((int)(1000 * scale), area.Height));
        MinimumSize = new Size((int)(420 * scale), (int)(600 * scale));

        web = new WebView2();
        web.Dock = DockStyle.Fill;
        web.DefaultBackgroundColor = Panel;
        Controls.Add(web);

        Load += async (s, e) => await StartAsync();
    }

    async Task StartAsync()
    {
        string appDir = AppDomain.CurrentDomain.BaseDirectory;
        string dataDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Subfloor");
        try
        {
            CoreWebView2Environment env = await CoreWebView2Environment.CreateAsync(null, dataDir, null);
            await web.EnsureCoreWebView2Async(env);
        }
        catch (WebView2RuntimeNotFoundException)
        {
            MessageBox.Show(this,
                "Subfloor needs the Microsoft Edge WebView2 Runtime, which is normally part of Windows 10 and 11.\n\n" +
                "Install it from Microsoft (search for \"WebView2 Runtime\"), then open Subfloor again.",
                "Subfloor", MessageBoxButtons.OK, MessageBoxIcon.Error);
            Close();
            return;
        }

        CoreWebView2 core = web.CoreWebView2;
        core.Settings.AreDevToolsEnabled = false;
        core.Settings.AreDefaultContextMenusEnabled = false;
        core.Settings.IsStatusBarEnabled = false;
        core.Settings.AreBrowserAcceleratorKeysEnabled = false;
        core.Settings.IsReputationCheckingRequired = false;
        core.NewWindowRequested += (s, e) => { e.Handled = true; };
        core.SetVirtualHostNameToFolderMapping(Host, Path.Combine(appDir, "web"), CoreWebView2HostResourceAccessKind.Deny);
        core.Navigate("https://" + Host + "/index.html");
        web.Focus();
    }
}
