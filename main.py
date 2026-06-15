 
"""
Главный модуль приложения для управления конфигурациями сетевых устройств.
"""

import os
from config_manager import ConfigManager

def print_separator():
    """Печатает разделительную линию."""
    print("-+" * 60)

def demonstrate_first_router(manager: ConfigManager):
    """Демонстрирует работу с первым маршрутизатором."""
    print("\nДемонстрация работы с первым маршрутизатором")
    print_separator()
    
    # Получаем первую конфигурацию
    configs_generator = manager.read_configs_generator()
    first_config = next(configs_generator)
    
    print(f"\n   Анализ конфигурации: {first_config['hostname']}")
    print(f"   SNMP community: {first_config['snmp']['community']}")
    
    # Задача 1: Изменяем статус интерфейса
    print("\nЗадача 1: Изменение статуса интерфейса GigabitEthernet0/1")
    # Ищем интерфейс GigabitEthernet0/1 или любой другой down интерфейс
    target_interface = None
    for iface_name, iface_data in first_config['interfaces'].items():
        if iface_data['status'] == 'down':
            target_interface = iface_name
            break
    
    if target_interface:
        if manager.modify_interface_status(first_config, target_interface, "up", "10.0.0.2"):
            print(f"   ✅ Интерфейс {target_interface} активирован")
    else:
        print("   ℹ️ Все интерфейсы уже в статусе up")
    
    # Задача 2: Добавляем новый интерфейс
    print("\nЗадача 2: Добавление нового интерфейса GigabitEthernet0/2")
    if manager.add_interface(first_config, "GigabitEthernet0/2", "192.168.2.1", "up"):
        print(f"   ✅ Добавлен интерфейс GigabitEthernet0/2")
    
    # Задача 3: Проверяем SNMP уязвимость
    print("\nЗадача 3: Проверка SNMP уязвимости")
    if manager.fix_snmp_vulnerability(first_config):
        print(f"   ✅ Исправлена SNMP уязвимость (public -> private)")
    else:
        print(f"   ✅ SNMP настроен безопасно (community: {first_config['snmp']['community']})")
    
    # Задача 4: Статистика трафика
    print("\nЗадача 4: Статистика трафика")
    traffic = manager.calculate_traffic_stats(first_config)
    print(f"   📊 Общий трафик: {traffic['total_traffic_mb']} MB")
    print(f"   📥 Входящий трафик: {traffic['total_in_mb']} MB")
    print(f"   📤 Исходящий трафик: {traffic['total_out_mb']} MB")
    print(f"   🔥 Самый загруженный интерфейс: {traffic['most_loaded_interface']} "
          f"({traffic['most_loaded_traffic_mb']} MB)")
    
    # Задача 5: Статусы интерфейсов
    print("\nЗадача 5: Статусы интерфейсов")
    status = manager.count_interface_status(first_config)
    print(f"   🟢 Интерфейсов UP: {status['up']} ({status['up_percentage']}%)")
    print(f"   🔴 Интерфейсов DOWN: {status['down']} ({status['down_percentage']}%)")
    
    # Задача 6: Анализ ACL
    print("\nЗадача 6: Анализ ACL")
    acl = manager.analyze_acls(first_config)
    print(f"   🔒 Интерфейсов с ACL: {acl['interfaces_with_acl']}")
    print(f"   🚫 Интерфейсов с DENY_ALL: {acl['interfaces_with_deny_all']}")
    
    # Задача 7: Метрики маршрутов
    print("\nЗадача 7: Метрики статических маршрутов")
    metrics = manager.calculate_routing_metrics(first_config)
    print(f"    Суммарная метрика: {metrics['total_metric']}")
    print(f"    Средняя метрика: {metrics['average_metric']}")
    
    # Задача 8: Валидация маршрутов
    print("\n Задача 8: Валидация маршрутов")
    is_valid, message = manager.validate_routes(first_config)
    print(f"   {message}")
    
    # Задача 9: Анализ заблокированных IP
    print("\n Задача 9: Анализ заблокированных IP")
    blocked = manager.analyze_blocked_ips(first_config)
    print(f"   🚫 Всего заблокированных IP: {blocked['total_blocked_ips']}")
    print(f"Топ-3 подсети:")
    for i, subnet_info in enumerate(blocked['top_3_subnets'], 1):
        print(f"      {i}. {subnet_info['subnet']}.x.x - {subnet_info['count']} IP")
    
    # Задача 10: Время работы и загрузка
    print("\n Задача 10: Время работы и загрузка")
    system = manager.calculate_uptime_cpu_memory(first_config)
    print(f"   Время работы: {system['uptime_days']} дней")
    print(f"   Загрузка CPU: {system['cpu_usage']}%")
    print(f"   Загрузка памяти: {system['memory_usage']}%")

def main():
    """Основная функция приложения."""
    print_separator()
    print("   УПРАВЛЕНИЕ КОНФИГУРАЦИЕЙ СЕТЕВЫХ УСТРОЙСТВ")
    print_separator()
    
    data_file = "router_configs.json"
    
    if not os.path.exists(data_file):
        print(f"\nФайл '{data_file}' не найден.")
        print("Запустите сначала python data_generator.py")
        return
    
    try:
        # Создаем менеджер конфигураций
        print("\nЗагрузка конфигураций...")
        manager = ConfigManager(data_file)
        
        # Демонстрируем работу с первым маршрутизатором
        demonstrate_first_router(manager)
        
        # Генерируем полный отчет
        print("\n" + "=" * 60)
        print("ГЕНЕРАЦИЯ ПОЛНОГО ОТЧЕТА")
        print_separator()
        manager.generate_report("analysis_report.json")
        
        # Сохраняем состояние менеджера
        print("\nСохранение состояния...")
        manager.save_state("manager_state.json")
        
        print("\n" + "=" * 60)
        print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ УСПЕШНО!")
        print("=" * 60)
        print("\nСозданные файлы:")
        print("   - router_configs.json (исходные данные)")
        print("   - analysis_report.json (аналитический отчет)")
        print("   - manager_state.json (состояние менеджера)")
        print("   - app.log (логи приложения)")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()