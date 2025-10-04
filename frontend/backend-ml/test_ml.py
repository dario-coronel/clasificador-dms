"""
Test del backend ML con OCR completo
"""
print("=" * 50)
print("Test de Backend ML con OCR")
print("=" * 50)

print("\n[1/4] Importando ocr_service...")
try:
    from ocr_service import ocr_service
    print("✓ OCR Service completo importado correctamente")
except Exception as e:
    print(f"✗ Error al importar OCR Service: {e}")
    import traceback
    traceback.print_exc()

print("\n[2/4] Verificando Tesseract...")
try:
    import pytesseract
    version = pytesseract.get_tesseract_version()
    print(f"✓ Tesseract disponible: {version}")
except Exception as e:
    print(f"⚠ Tesseract no disponible: {e}")
    print("  Instala Tesseract OCR desde: https://github.com/UB-Mannheim/tesseract/wiki")

print("\n[3/4] Importando classifier_service...")
try:
    from classifier_service import classifier
    print("✓ Classifier Service importado correctamente")
except Exception as e:
    print(f"✗ Error al importar Classifier: {e}")
    import traceback
    traceback.print_exc()

print("\n[4/4] Probando clasificador...")
try:
    text = "Este es un contrato de arrendamiento entre las partes mencionadas."
    category, confidence, probs = classifier.classify_document(text)
    print(f"✓ Clasificación exitosa: {category} ({confidence:.2%})")
except Exception as e:
    print(f"✗ Error al clasificar: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test completado")
print("=" * 50)
