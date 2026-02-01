#!/usr/bin/env python3
"""
CLI para RegrasEngine

Versão: 1.0
Data: 2026-01-31
"""

import sys
import os
import argparse

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from regras.engine import RegrasEngine
from regras.logger import RuleLogger


def cmd_load(args):
    """Comando: load"""
    print(f"📥 Carregando regras de {args.rules_dir}...")
    engine = RegrasEngine(rules_dir=args.rules_dir)
    total = engine.count_rules()
    print(f"✅ {total} regras carregadas")


def cmd_evaluate(args):
    """Comando: evaluate"""
    engine = RegrasEngine(rules_dir=args.rules_dir)
    
    # Parse contexto
    contexto = {}
    for item in args.context:
        if '=' in item:
            key, value = item.split('=', 1)
            # Tenta converter para número
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                pass
            contexto[key] = value
    
    print(f"🔍 Avaliando contexto: {contexto.get('modulo', 'unknown')}")
    acoes = engine.evaluate(contexto)
    
    print(f"\n🎯 {len(acoes)} ações executadas:")
    for acao in acoes:
        print(f"  - {acao['rule_id']}: {acao['acao']} (prioridade: {acao.get('prioridade', 'normal')})")


def cmd_reload(args):
    """Comando: reload"""
    engine = RegrasEngine(rules_dir=args.rules_dir)
    print("🔄 Recarregando regras...")
    count = engine.reload()
    print(f"✅ {count} regras recarregadas")


def cmd_history(args):
    """Comando: history"""
    logger = RuleLogger()
    history = logger.get_history(rule_id=args.rule_id, limit=args.limit)
    
    print(f"\n📜 Histórico de decisões:")
    for decision in history:
        print(f"\n  [{decision[1]}] {decision[3]}: {decision[6]}")
        print(f"    Regra: {decision[2]}")
        print(f"    Ação: {decision[5]}")


def cmd_test(args):
    """Comando: test"""
    engine = RegrasEngine(rules_dir=args.rules_dir)
    
    # Parse contexto
    contexto = {}
    if args.context:
        for item in args.context:
            if '=' in item:
                key, value = item.split('=', 1)
                try:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                except ValueError:
                    pass
                contexto[key] = value
    
    print(f"🧪 Testando regra {args.rule_id}...")
    print(f"    Contexto: {contexto}")
    
    # Busca regra
    for rule_set_name, rule_set in engine.rules.items():
        regras_dict = rule_set.get('regras', {})
        if isinstance(regras_dict, dict):
            for cat, regras in regras_dict.items():
                for rule in regras:
                    if rule.get('id') == args.rule_id:
                        print(f"\n    Regra encontrada:")
                        print(f"      ID: {rule['id']}")
                        print(f"      Módulo: {rule['modulo']}")
                        print(f"      Categoria: {rule['categoria']}")
                        print(f"      Condição: {rule['condicao']}")
                        print(f"      Ação: {rule['acao']}")
                        print(f"      Prioridade: {rule.get('prioridade', 'normal')}")
                        print(f"      Descrição: {rule.get('descricao', 'N/A')}")
                        return
    
    print(f"❌ Regra {args.rule_id} não encontrada")
    sys.exit(1)


def cmd_stats(args):
    """Comando: stats"""
    engine = RegrasEngine(rules_dir=args.rules_dir)
    total = engine.count_rules()
    
    print(f"\n📊 Estatísticas de Regras:")
    print(f"  Total de regras: {total}")
    
    # Por rule set
    print(f"\n  Por Rule Set:")
    for rule_set_name, rule_set in engine.rules.items():
        regras_dict = rule_set.get('regras', {})
        if isinstance(regras_dict, dict):
            count = sum(len(regras) for regras in regras_dict.values() if isinstance(regras, list))
            print(f"    {rule_set_name}: {count} regras")
    
    # Por categoria
    print(f"\n  Por Categoria:")
    categories = {}
    for rule_set in engine.rules.values():
        regras_dict = rule_set.get('regras', {})
        if isinstance(regras_dict, dict):
            for cat, regras in regras_dict.items():
                if isinstance(regras, list):
                    categories[cat] = categories.get(cat, 0) + len(regras)
    
    for cat, count in sorted(categories.items()):
        print(f"    {cat}: {count} regras")
    
    # Por módulo
    print(f"\n  Por Módulo:")
    modules = {}
    for rule_set in engine.rules.values():
        regras_dict = rule_set.get('regras', {})
        if isinstance(regras_dict, dict):
            for regras in regras_dict.values():
                if isinstance(regras, list):
                    for rule in regras:
                        modulo = rule.get('modulo', 'unknown')
                        modules[modulo] = modules.get(modulo, 0) + 1
    
    for mod, count in sorted(modules.items()):
        print(f"    {mod}: {count} regras")


def cmd_list(args):
    """Comando: list"""
    engine = RegrasEngine(rules_dir=args.rules_dir)
    
    if args.category:
        rules = engine.get_rules_by_category(args.category)
        print(f"\n📋 Regras da categoria '{args.category}':")
        for rule in rules:
            print(f"  - {rule['id']}: {rule['acao']} ({rule.get('prioridade', 'normal')})")
    elif args.module:
        rules = engine.get_rules_by_module(args.module)
        print(f"\n📋 Regras do módulo '{args.module}':")
        for rule in rules:
            print(f"  - {rule['id']}: {rule['acao']} ({rule.get('prioridade', 'normal')})")
    else:
        print(f"\n📋 Todas as regras:")
        for rule_set_name, rule_set in engine.rules.items():
            print(f"\n  {rule_set_name}:")
            regras_dict = rule_set.get('regras', {})
            if isinstance(regras_dict, dict):
                for cat, regras in regras_dict.items():
                    print(f"    {cat}:")
                    for rule in regras:
                        print(f"      - {rule['id']}: {rule['acao']} ({rule.get('prioridade', 'normal')})")


def main():
    """Main"""
    parser = argparse.ArgumentParser(description="CLI para RegrasEngine")
    parser.add_argument('--rules-dir', default='rules', help='Diretório das regras')
    
    subparsers = parser.add_subparsers(dest='command', help='Comando')
    
    # load
    subparsers.add_parser('load', help='Carrega regras')
    
    # evaluate
    eval_parser = subparsers.add_parser('evaluate', help='Avalia contexto')
    eval_parser.add_argument('--context', nargs='+', required=True, help='Contexto (ex: modulo=rastreador sources_collected=10000)')
    
    # reload
    subparsers.add_parser('reload', help='Recarrega regras')
    
    # history
    history_parser = subparsers.add_parser('history', help='Histórico de decisões')
    history_parser.add_argument('--rule-id', help='Filtrar por rule ID')
    history_parser.add_argument('--limit', type=int, default=20, help='Limite de resultados')
    
    # test
    test_parser = subparsers.add_parser('test', help='Testa regra específica')
    test_parser.add_argument('rule_id', help='ID da regra para testar')
    test_parser.add_argument('--context', nargs='*', help='Contexto para avaliar')
    
    # stats
    subparsers.add_parser('stats', help='Estatísticas de regras')
    
    # list
    list_parser = subparsers.add_parser('list', help='Lista regras')
    list_parser.add_argument('--category', help='Filtrar por categoria')
    list_parser.add_argument('--module', help='Filtrar por módulo')
    
    args = parser.parse_args()
    
    if args.command == 'load':
        cmd_load(args)
    elif args.command == 'evaluate':
        cmd_evaluate(args)
    elif args.command == 'reload':
        cmd_reload(args)
    elif args.command == 'history':
        cmd_history(args)
    elif args.command == 'test':
        cmd_test(args)
    elif args.command == 'stats':
        cmd_stats(args)
    elif args.command == 'list':
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
