from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Core del Sistema'
    
    def ready(self):
        """
        Se ejecuta cuando Django inicia
        Aquí conectamos las signals de auditoría
        """
        # Importar signals para que se conecten
        import core.signals
        
        print("✅ Signals de auditoría conectadas correctamente")
