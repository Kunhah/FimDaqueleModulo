def mostrar_relatorio_limpeza(relatorio: dict) -> None:
    removidos = relatorio['removidos']
    print('\n=== RELATORIO DE LIMPEZA ===')
    print(f'Registros iniciais: {relatorio["iniciais"]}')
    print(f'Total removido: {len(removidos)}')
    print(f'Registros finais: {relatorio["finais"]}')
    print(f'Clientes sinalizados fora do padrao: {relatorio["clientes_sinalizados"]}')
    print('\nRemovidos por motivo:')
    print(removidos['motivo'].value_counts().to_string())
    print('\nRegistros removidos:')
    print(removidos.to_string(index=False))
