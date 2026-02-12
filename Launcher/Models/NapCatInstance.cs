using System.Diagnostics;

namespace MultiEchoLauncher.Models;

internal sealed class NapCatInstance(string name)
{
    private int _webUiOpened;

    public string Name { get; } = name;
    public Process? Process { get; set; }
    public string? WebUiUrl { get; private set; }

    public bool TrySetWebUiUrl(string url)
    {
        if (Interlocked.CompareExchange(ref _webUiOpened, 1, 0) != 0)
            return false;

        WebUiUrl = url;
        return true;
    }

    public string Status => Process is { HasExited: false } ? "Running" : "Stopped";
    public string PidDisplay => Process?.Id.ToString() ?? "N/A";
}
