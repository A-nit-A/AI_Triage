import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Script principal para ejecutar la automatización.")
    parser.add_argument('--force-rag', action='store_true', help="Fuerza la ejecución de rag.py para recrear la base de datos chroma_db.")
    args = parser.parse_args()

    # Obtener la ruta del directorio base donde está este script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    automation_dir = os.path.join(base_dir, 'automation')
    chroma_db_dir = os.path.join(automation_dir, 'chroma_db')
    
    rag_script = os.path.join(automation_dir, 'rag.py')
    agent_script = os.path.join(automation_dir, 'agent.py')
    
    if args.force_rag or not os.path.exists(chroma_db_dir):
        motivo = "se usó el parámetro --force-rag" if args.force_rag else f"el directorio '{chroma_db_dir}' no existe"
        print(f"Ejecutando rag.py porque {motivo}...")
        try:
            subprocess.run([sys.executable, rag_script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar rag.py: {e}")
            sys.exit(1)
    else:
        print(f"El directorio '{chroma_db_dir}' existe. Omitiendo la ejecución de rag.py.")
        
    print("Ejecutando agent.py...")
    try:
        subprocess.run([sys.executable, agent_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar agent.py: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
