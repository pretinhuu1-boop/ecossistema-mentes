#!/usr/bin/env python3
import argparse
import sys
import os
import json

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from rastreador.crawler import Rastreador
    from minerador.extractor import Minerador
    # Placeholder imports for future modules
    # from construtor.mind_builder import MindBuilder
    # from squads.generator import SquadGenerator
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def run_rastreador(args):
    print(f"🚀 Iniciando Rastreador... (Target: {args.target})")
    r = Rastreador()
    # In a real scenario, we would pass args.target to run()
    r.run()
    return {"status": "completed", "module": "rastreador"}

def run_minerador(args):
    print(f"⛏️ Iniciando Minerador... (Source: {args.source})")
    m = Minerador()
    # In a real scenario, we would pass args.source
    result = m.process_batch()
    return {"status": "completed" if result else "stopped", "module": "minerador"}

def run_mind_builder(args):
    print(f"🧠 Construindo Mente para: {args.author}")
    # Mock implementation
    mind_id = f"mind_{args.author.lower().replace(' ', '_')}_v1"
    print(f"✅ Mente criada: {mind_id}")
    return {"status": "completed", "mind_id": mind_id}

def run_squad_task(args):
    print(f"🤖 Squad Executing Task: {args.task}")
    print(f"   Context: Mind={args.mind_id}, Skill={args.skill}")
    # Mock execution
    return {"status": "completed", "output": f"Executed '{args.task}' using {args.skill}"}

def main():
    parser = argparse.ArgumentParser(description="Ecossistema Mentes CLI")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Rastreador
    p_track = subparsers.add_parser("rastrear", help="Executa o rastreador")
    p_track.add_argument("--target", help="Alvo do rastreamento", default="all")
    p_track.set_defaults(func=run_rastreador)

    # Minerador
    p_mine = subparsers.add_parser("minerar", help="Executa o minerador")
    p_mine.add_argument("--source", help="Fonte de dados", default="latest")
    p_mine.set_defaults(func=run_minerador)

    # Construtor
    p_build = subparsers.add_parser("construir_mente", help="Constrói uma mente")
    p_build.add_argument("--author", required=True, help="Nome do autor")
    p_build.set_defaults(func=run_mind_builder)

    # Squads
    p_squad = subparsers.add_parser("squad_task", help="Executa tarefa via squad")
    p_squad.add_argument("--mind_id", required=True, help="ID da Mente")
    p_squad.add_argument("--skill", required=True, help="Skill a ser usada")
    p_squad.add_argument("--task", required=True, help="Descrição da tarefa")
    p_squad.set_defaults(func=run_squad_task)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        result = args.func(args)
        print(json.dumps(result)) # Output JSON for the Gateway to parse
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
