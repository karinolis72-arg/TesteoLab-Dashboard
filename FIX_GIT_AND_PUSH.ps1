# =====================================================
# SCRIPT PARA REPARAR Y HACER PUSH A GITHUB
# Ejecutar en PowerShell como Administrador
# Fecha: 11 Abril 2026
# =====================================================

Write-Host "🔧 Reparando repositorio Git y haciendo push..." -ForegroundColor Cyan

# Paso 1: Limpiar el repositorio corrupto
Write-Host "`n1️⃣  Limpiando repositorio .git corrupto..." -ForegroundColor Yellow
Remove-Item -Path ".git" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "   ✅ .git removido" -ForegroundColor Green

# Paso 2: Inicializar repositorio nuevo
Write-Host "`n2️⃣  Inicializando nuevo repositorio Git..." -ForegroundColor Yellow
git init
git config user.name "Karina"
git config user.email "karinolis72@gmail.com"
Write-Host "   ✅ Repositorio inicializado" -ForegroundColor Green

# Paso 3: Agregar remote
Write-Host "`n3️⃣  Agregando remote origin..." -ForegroundColor Yellow
git remote add origin https://github.com/karinolis/TesteoLab-Dashboard.git
Write-Host "   ✅ Remote agregado" -ForegroundColor Green

# Paso 4: Cambiar rama a main
Write-Host "`n4️⃣  Configurando rama main..." -ForegroundColor Yellow
git branch -M main
Write-Host "   ✅ Rama configurada" -ForegroundColor Green

# Paso 5: Agregar archivos
Write-Host "`n5️⃣  Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "   ✅ Archivos agregados" -ForegroundColor Green

# Paso 6: Hacer commit
Write-Host "`n6️⃣  Haciendo commit..." -ForegroundColor Yellow
git commit -m "Fix: Remove sensitive token from documentation - use placeholder instead"
Write-Host "   ✅ Commit realizado" -ForegroundColor Green

# Paso 7: Push a GitHub
Write-Host "`n7️⃣  Haciendo push a GitHub..." -ForegroundColor Yellow
Write-Host "   ⚠️  Se abrirá ventana de autenticación de GitHub" -ForegroundColor Magenta
Write-Host "   📝 Usa tu Personal Access Token (PAT) como contraseña" -ForegroundColor Magenta
Write-Host "   📝 Username: tu-usuario-github" -ForegroundColor Magenta
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ ¡PUSH EXITOSO!" -ForegroundColor Green
    Write-Host "`n   📍 Siguiente paso: Ir a Render.com y crear Web Service" -ForegroundColor Cyan
    Write-Host "   📍 Ver instrucciones en: QUICK_START_RENDER.md" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Error en push. Verifica credenciales y conexión." -ForegroundColor Red
    Write-Host "`n   🔍 Si necesitas ayuda, revisa: README_INICIO.md" -ForegroundColor Yellow
}

Write-Host "`n" -ForegroundColor White
pause
