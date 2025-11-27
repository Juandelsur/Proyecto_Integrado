<template>
  <div class="home-view">
    <div class="container">
      <div class="content-card">
        <div class="icon-wrapper">
          <i class="bi bi-house-door"></i>
        </div>
        <h1 class="title">🏥 SCA Hospital</h1>
        <p class="subtitle">Sistema de Control de Activos</p>
        <p class="description">Dashboard principal en construcción.</p>
        <div class="actions">
          <button @click="$router.push('/escanear')" class="btn-primary">
            <i class="bi bi-qr-code-scan"></i>
            <span>Escanear QR</span>
          </button>
          <button @click="$router.push('/inventario')" class="btn-secondary">
            <i class="bi bi-list-ul"></i>
            <span>Ver Inventario</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Placeholder para HomeView (Dashboard)
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.container {
  width: 100%;
  max-width: 600px;
}

.content-card {
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.icon-wrapper {
  width: 100px;
  height: 100px;
  margin: 0 auto 2rem;
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper i {
  font-size: 3rem;
  color: white;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1565c0;
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-primary,
.btn-secondary {
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.btn-primary {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(13, 71, 161, 0.6);
}

.btn-secondary {
  background: white;
  color: #1565c0;
  border: 2px solid #1565c0;
}

.btn-secondary:hover {
  background: #f5f5f5;
  transform: translateY(-2px);
}

.btn-primary i,
.btn-secondary i {
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .content-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>
