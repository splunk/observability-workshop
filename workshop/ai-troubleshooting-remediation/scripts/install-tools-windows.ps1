param(
    [switch]$IncludeWsl
)

$ErrorActionPreference = "Stop"

function Install-WingetPackage {
    param(
        [string]$Id,
        [string]$Name
    )

    Write-Host "Installing or updating $Name..."
    winget install --id $Id --exact --accept-package-agreements --accept-source-agreements --silent `
        -e 2>$null
    if ($LASTEXITCODE -ne 0) {
        winget upgrade --id $Id --exact --accept-package-agreements --accept-source-agreements --silent `
            -e 2>$null
    }
}

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw "winget is required. Install App Installer from the Microsoft Store, then rerun this script."
}

Install-WingetPackage -Id "Git.Git" -Name "Git"
Install-WingetPackage -Id "Docker.DockerDesktop" -Name "Docker Desktop"
Install-WingetPackage -Id "Kubernetes.kubectl" -Name "kubectl"
Install-WingetPackage -Id "Helm.Helm" -Name "Helm"
Install-WingetPackage -Id "Kubernetes.kind" -Name "kind"
Install-WingetPackage -Id "Kubernetes.minikube" -Name "Minikube"

if ($IncludeWsl) {
    Write-Host "Installing WSL with Ubuntu. A restart may be required."
    wsl --install -d Ubuntu
}

Write-Host ""
Write-Host "Start Docker Desktop before deploying the lab app."
Write-Host "Open a new PowerShell window, then verify tools with:"
Write-Host "  git --version"
Write-Host "  docker version"
Write-Host "  kubectl version --client"
Write-Host "  helm version"
Write-Host "  kind version"
Write-Host "  minikube version"

