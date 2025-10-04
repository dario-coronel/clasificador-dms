"""
Script para regenerar el modelo de clasificación con las nuevas categorías
"""
import sys
import os

# Asegurar que estamos en el directorio correcto
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from classifier_service import DocumentClassifier

print("=" * 60)
print("Regenerando modelo de clasificación...")
print("=" * 60)
print()

# Crear instancia del clasificador
# Esto automáticamente creará un nuevo modelo si no existe
classifier = DocumentClassifier()

print("✅ Modelo regenerado exitosamente")
print()
print("Categorías disponibles:")
for i, category in enumerate(classifier.categories, 1):
    print(f"  {i}. {category}")
print()
print("=" * 60)
