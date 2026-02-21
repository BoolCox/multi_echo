using System.Text.RegularExpressions;
using Launcher.Services;

Console.Title = "Multi Echo Candy Launcher";

using var job = new Job();
var napcat = new NapCatManager(job);
var nonebot = new NonebotManager(job);
var exitRequested = false;

Console.CancelKeyPress += (_, e) =>
{
    e.Cancel = true;
    exitRequested = true;
};
AppDomain.CurrentDomain.ProcessExit += (_, _) => job.Dispose();

var currentDir = Directory.GetCurrentDirectory();
var napcatDirs = Directory.GetDirectories(currentDir)
    .Where(d => NapCatFolderRegex().IsMatch(Path.GetFileName(d)))
    .Order()
    .ToArray();

if (napcatDirs.Length == 0)
{
    Console.WriteLine("No NapCat folders found (napcat1, napcat2, ...)");
    Console.ReadKey();
    return;
}

Console.WriteLine($"Found {napcatDirs.Length} NapCat instance(s):");
foreach (var dir in napcatDirs)
    Console.WriteLine($" - {Path.GetFileName(dir)}");

LinkConfigs(napcatDirs);

Console.WriteLine("\nStarting...\n");
nonebot.Start(currentDir);
napcat.LaunchAll(napcatDirs);

while (!exitRequested)
{
    napcat.OpenPendingBrowsers();
    Console.Clear();
    Console.WriteLine("NapCat status:\n");
    Console.WriteLine($"[nonebot] PID={nonebot.PidDisplay,-6} Status={nonebot.Status}");
    Console.WriteLine();

    foreach (var inst in napcat.Instances)
    {
        Console.WriteLine(
            $"[{inst.Name}] PID={inst.PidDisplay,-6} Status={inst.Status,-8} WebUI={inst.WebUiUrl ?? "waiting..."}");
    }

    Thread.Sleep(1000);
}

static void LinkConfigs(string[] dirs)
{
    var primary = Path.Combine(dirs[0], "config");
    foreach (var dir in dirs.Skip(1))
    {
        var link = Path.Combine(dir, "config");
        var name = Path.GetFileName(dir);
        try
        {
            if (Directory.Exists(link) || File.Exists(link))
            {
                if ((File.GetAttributes(link) & FileAttributes.ReparsePoint) != 0)
                    continue;
                Directory.Delete(link, true);
            }
            Directory.CreateSymbolicLink(link, primary);
            Console.WriteLine($"[{name}] config linked to {primary}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[{name}] config link failed: {ex.Message}");
        }
    }
}

partial class Program
{
    [GeneratedRegex(@"^napcat\d+$", RegexOptions.IgnoreCase)]
    private static partial Regex NapCatFolderRegex();
}
