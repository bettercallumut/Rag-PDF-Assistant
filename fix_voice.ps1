# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Yonetici haklari gerekiyor. Yeniden baslatiliyor..."
    Start-Process PowerShell -Verb RunAs -ArgumentList "-File `"$PSCommandPath`""
    Exit
}

Write-Host "Turkce Dil Paketi Kontrol Ediliyor..."

# Check if Turkish Language Pack is installed
$lang = Get-WindowsCapability -Online | Where-Object { $_.Name -like "Language.Basic~~~tr-TR~*" }

if ($lang.State -eq "Installed") {
    Write-Host "Turkce dil paketi zaten yuklu."
} else {
    Write-Host "Turkce dil paketi yukleniyor... Lutfen bekleyin."
    Add-WindowsCapability -Online -Name $lang.Name
    Write-Host "Dil paketi yuklendi."
}

# Check TTS Voices specifically
$tts = Get-WindowsCapability -Online | Where-Object { $_.Name -like "Language.TextToSpeech~~~tr-TR~*" }
if ($tts.State -eq "Installed") {
    Write-Host "Turkce TTS sesi zaten yuklu."
} else {
    Write-Host "Turkce TTS sesi yukleniyor..."
    Add-WindowsCapability -Online -Name $tts.Name
    Write-Host "TTS sesi yuklendi."
}

# Registry fix for pyttsx3 (OneCore voices visibility)
Write-Host "pyttsx3 icin Registry ayarlari kontrol ediliyor..."
$sourcePath = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
$destPath = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens"

if (Test-Path $sourcePath) {
    Copy-Item -Path "$sourcePath\*" -Destination $destPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Sesler kopyalandi."
}

Write-Host "Islem Tamamlandi. Pencere kapaniyor..."
Start-Sleep -Seconds 3
