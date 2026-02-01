import argparse
import json
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from termination import Termination

def main():
    parser = argparse.ArgumentParser(description="CLI do Sistema de Parada (GAP 11)")
    subparsers = parser.add_subparsers(dest="command", help="Comandos")

    # Comando: list
    subparsers.add_parser("list", help="Lista todos os critérios configurados")

    # Comando: add
    add_parser = subparsers.add_parser("add", help="Adiciona um novo critério de parada")
    add_parser.add_argument("--module", required=True, help="Nome do módulo")
    add_parser.add_argument("--name", required=True, help="Nome da métrica")
    add_parser.add_argument("--type", required=True, help="Tipo (absolute/minimum/etc)")
    add_parser.add_argument("--threshold", required=True, type=float, help="Threshold numérico")
    add_parser.add_argument("--operator", default=">=", help="Operador (>=, <=, ==, etc)")
    add_parser.add_argument("--description", help="Descrição do critério")

    # Comando: history
    hist_parser = subparsers.add_parser("history", help="Mostra histórico de paradas")
    hist_parser.add_argument("--module", help="Filtrar por módulo")
    hist_parser.add_argument("--limit", type=int, default=10, help="Limite de registros")

    # Comando: stats
    subparsers.add_parser("stats", help="Mostra estatísticas de paradas")

    args = parser.parse_args()
    
    term = Termination()

    if args.command == "list":
        criteria_list = term.criteria.get_all()
        if not criteria_list:
            print("📭 Nenhum critério cadastrado.")
        else:
            print(json.dumps(criteria_list, indent=2))

    elif args.command == "add":
        criterion = {
            "module": args.module,
            "name": args.name,
            "type": args.type,
            "threshold": args.threshold,
            "operator": args.operator,
            "description": args.description or ""
        }
        term.criteria.create_criterion(criterion)
        print(f"✅ Critério '{args.name}' para o módulo '{args.module}' criado com sucesso.")

    elif args.command == "check":
        try:
            metrics = json.loads(args.metrics)
            met = term.evaluate(args.module, metrics)
            if met:
                print(f"🛑 Módulo {args.module} DEVE parar. {len(met)} critérios atingidos.")
            else:
                print(f"✅ Módulo {args.module} pode continuar.")
        except Exception as e:
            print(f"❌ Erro ao processar métricas: {e}")

    elif args.command == "history":
        history = term.get_history(module=args.module, limit=args.limit)
        print(json.dumps(history, indent=2))

    elif args.command == "stats":
        stats = term.get_stats()
        print(json.dumps(stats, indent=2))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
