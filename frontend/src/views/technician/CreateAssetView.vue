<template>
  <div class="placeholder-view">
    <div class="container">
      <div class="content-card">
        <div class="icon-wrapper">
          <i class="bi bi-plus-circle"></i>
        </div>
        <h1 class="title">➕ Crear Nuevo Activo</h1>
        <p class="subtitle">Vista de Creación</p>
        <p class="description">Esta funcionalidad estará lista pronto.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// Placeholder para CreateAssetView (Técnico)
</script>

<style scoped>
.placeholder-view {
  min-height: calc(100vh - 112px);
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

