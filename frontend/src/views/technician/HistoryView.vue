<template>
  <div class="placeholder-view">
    <div class="container">
      <div class="content-card">
        <div class="icon-wrapper">
          <i class="bi bi-clock-history"></i>
        </div>
        <h1 class="title">🚧 En Construcción 🚧</h1>
        <p class="subtitle">Vista de Histórico de Movimientos</p>
        <p class="description">Esta funcionalidad estará lista pronto.</p>
        <button @click="$router.push('/tecnico/home')" class="btn-back">
          <i class="bi bi-house-door"></i>
          <span>Volver al Inicio</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// Placeholder para HistoryView (Técnico)
</script>

<style scoped>
.placeholder-view {
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

.btn-back {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.4);
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(13, 71, 161, 0.6);
}

.btn-back i {
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

