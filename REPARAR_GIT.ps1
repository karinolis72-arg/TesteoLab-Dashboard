Write-Host "Reparando repositorio Git..." -ForegroundColor Cyan

# Paso 1: Limpiar .git corrupto
Write-Host "`nPaso 1: Limpiando repositorio .git..." -ForegroundColor Yellow
Remove-Item -Path ".git" -Recurse -Force -ErrorAction SilentlyContinue

# Paso 2: Inicializar nuevo repo
Write-Host "`nPaso 2: Inicializando nuevo repositorio..." -ForegroundColor Yellow
git init
git config user.name "Karina"
git config user.email "karinolis72@gmail.com"

# Paso 3: Agregar remote
Write-Host "`nPaso 3: Agregando remote..." -ForegroundColor Yellow
git remote add origin https://github.com/karinolis/TesteoLab-Dashboard.git

# Paso 4: Configurar rama
Write-Host "`nPaso 4: Configurando rama main..." -ForegroundColor Yellow
git branch -M main

# Paso 5: Agregar archivos
Write-Host "`nPaso 5: Agregando archivos..." -ForegroundColor Yellow
git add .

# Paso 6: Hacer commit
Write-Host "`nPaso 6: Haciendo commit..." -ForegroundColor Yellow
git commit -m "TesteoLab Dashboard - Sprint 1 v2.0 listo para deploy"

# Paso 7: Push a GitHub
Write-Host "`nPaso 7: Haciendo push a GitHub..." -ForegroundColor Yellow
Write-Host "Se abrira ventana de autenticacion - usa Personal Access Token" -ForegroundColor Magenta
git push -u origin main

Write-Host "`nProceso completado!" -ForegroundColor Green
pause
