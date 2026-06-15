"""
Управления конфигурацией сетевых устройств.
Содержит класс ConfigManager для анализа и модификации конфигураций маршрутизаторов.
"""

import json
import logging
from typing import Dict, Any, List, Generator, Optional, Tuple
from collections import Counter
from datetime import datetime
import os

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Класс для управления и анализа конфигураций сетевых устройств.
    """
    
    def __init__(self, file_path: str = "router_configs.json"):
        """
        Инициализация менеджера конфигураций.
        """
        self._configs = []
        self._current_index = 0
        self._file_path = file_path
        self._load_configs()
        logger.info(f"ConfigManager инициализирован с файлом {file_path}")
        print(f"---Загружено {len(self._configs)} конфигураций---")
    
    @property
    def configs_count(self) -> int:
        return len(self._configs)
    
    @property
    def file_path(self) -> str:
        return self._file_path
    
    def _load_configs(self) -> None:
        """Загружает конфигурации из файла."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as f:
                self._configs = json.load(f)
            logger.info(f"Загружено {len(self._configs)} конфигураций")
        except FileNotFoundError:
            logger.error(f"Файл {self._file_path} не найден")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            raise
    
    def read_configs_generator(self) -> Generator[Dict[str, Any], None, None]:
        """
        Генератор для последовательного чтения конфигураций.
        """
        for config in self._configs:
            logger.debug(f"Чтение конфигурации {config.get('hostname', 'Unknown')}")
            yield config
    
    # Задача 1: Изменить статус интерфейса
    def modify_interface_status(self, config: Dict[str, Any], interface: str, 
                               status: str, ip: Optional[str] = None) -> bool:
        """
        Изменяет статус интерфейса и опционально IP-адрес.
        """
        if interface in config['interfaces']:
            config['interfaces'][interface]['status'] = status
            if ip:
                config['interfaces'][interface]['ip'] = ip
            logger.info(f"✓ Изменен интерфейс {interface}: статус={status}, ip={ip}")
            return True
        else:
            logger.warning(f"X Интерфейс {interface} не найден")
            return False
    
    # Задача 2: Добавить новый интерфейс
    def add_interface(self, config: Dict[str, Any], interface: str, 
                     ip: str, status: str = 'up') -> bool:
        """
        Добавляет новый интерфейс в конфигурацию.
        """
        if interface not in config['interfaces']:
            config['interfaces'][interface] = {
                "ip": ip,
                "status": status,
                "acl_in": None,
                "traffic_in_mb": 0,
                "traffic_out_mb": 0
            }
            logger.info(f"✓ Добавлен новый интерфейс {interface} с IP {ip}")
            return True
        else:
            logger.warning(f"X Интерфейс {interface} уже существует")
            return False
    
    # Задача 3: Проверить и исправить SNMP уязвимость
    def fix_snmp_vulnerability(self, config: Dict[str, Any]) -> bool:
        """
        Исправляет уязвимость SNMP (community 'public').
        """
        if config['snmp']['community'] == 'public':
            config['snmp']['community'] = 'private'
            logger.warning(f"✓ Исправлена SNMP уязвимость: public -> private")
            return True
        return False
    
    # Задача 4: Подсчет трафика
    def calculate_traffic_stats(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитывает статистику трафика для всех интерфейсов.
        """
        total_in = 0
        total_out = 0
        max_interface = None
        max_traffic = -1
        
        for name, interface in config['interfaces'].items():
            total_in += interface['traffic_in_mb']
            total_out += interface['traffic_out_mb']
            interface_total = interface['traffic_in_mb'] + interface['traffic_out_mb']
            
            if interface_total > max_traffic:
                max_traffic = interface_total
                max_interface = name
        
        return {
            'total_traffic_mb': total_in + total_out,
            'total_in_mb': total_in,
            'total_out_mb': total_out,
            'most_loaded_interface': max_interface,
            'most_loaded_traffic_mb': max_traffic
        }
    
    # Задача 5: Подсчет статусов интерфейсов
    def count_interface_status(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подсчитывает количество интерфейсов в статусе up и down.
        """
        up_count = sum(1 for iface in config['interfaces'].values() if iface['status'] == 'up')
        down_count = len(config['interfaces']) - up_count
        total = len(config['interfaces'])
        
        return {
            'up': up_count,
            'down': down_count,
            'up_percentage': round((up_count / total * 100), 2) if total > 0 else 0,
            'down_percentage': round((down_count / total * 100), 2) if total > 0 else 0
        }
    
    # Задача 6: Анализ ACL
    def analyze_acls(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует настройки ACL на интерфейсах.
        """
        acl_configured = sum(1 for i in config['interfaces'].values()
                           if i['acl_in'] is not None)
        deny_all_count = sum(1 for i in config['interfaces'].values()
                           if i['acl_in'] == 'DENY_ALL')
        
        return {
            'interfaces_with_acl': acl_configured,
            'interfaces_with_deny_all': deny_all_count
        }
    
    # Задача 7: Метрики маршрутов
    def calculate_routing_metrics(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитывает статистику метрик статических маршрутов.
        """
        static_routes = config['routing']['static']
        if not static_routes:
            return {'total_metric': 0, 'average_metric': 0}
        
        total_metric = sum(route['metric'] for route in static_routes)
        average_metric = round(total_metric / len(static_routes), 2)
        
        return {
            'total_metric': total_metric,
            'average_metric': average_metric
        }
    
    # Задача 8: Валидация маршрутов
    def validate_routes(self, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Проверяет соответствие total_routes расчетному значению.
        """
        calculated = config['routing']['dynamic_routes'] + len(config['routing']['static'])
        actual = config['routing']['total_routes']
        
        if calculated != actual:
            message = (f"⚠️ Несоответствие маршрутов: расчетное={calculated}, "
                      f"фактическое={actual}")
            logger.warning(message)
            return False, message
        return True, "✓ Количество маршрутов корректно"
    
    # Задача 9: Анализ заблокированных IP
    def analyze_blocked_ips(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует заблокированные IP-адреса.
        """
        blocked_ips = config['security']['blocked_ips']
        
        # Извлекаем первые два октета для подсетей
        subnets = []
        for ip in blocked_ips:
            parts = ip.split('.')
            if len(parts) >= 2:
                subnet = f"{parts[0]}.{parts[1]}"
                subnets.append(subnet)
        
        subnet_counter = Counter(subnets)
        top_subnets = subnet_counter.most_common(3)
        
        return {
            'total_blocked_ips': len(blocked_ips),
            'top_3_subnets': [{'subnet': subnet, 'count': count} 
                            for subnet, count in top_subnets]
        }
    
    # Задача 10: Время работы и загрузка
    def calculate_uptime_cpu_memory(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Рассчитывает время работы в днях и среднюю загрузку.
        """
        days = config['uptime_seconds'] / 86400
        
        return {
            'uptime_days': round(days, 2),
            'cpu_usage': config['cpu_usage'],
            'memory_usage': config['memory_usage']
        }
    
    # Полный анализ одной конфигурации
    def analyze_all(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполняет полный анализ конфигурации.

        """
        logger.info(f"Начат анализ конфигурации {config.get('hostname', 'Unknown')}")
        
        report = {
            'hostname': config['hostname'],
            'timestamp': datetime.now().isoformat(),
            'modifications': {
                'snmp_vulnerability_fixed': self.fix_snmp_vulnerability(config)
            },
            'traffic_stats': self.calculate_traffic_stats(config),
            'interface_status': self.count_interface_status(config),
            'acl_analysis': self.analyze_acls(config),
            'routing_metrics': self.calculate_routing_metrics(config),
            'route_validation': self.validate_routes(config)[1],
            'blocked_ips_analysis': self.analyze_blocked_ips(config),
            'system_stats': self.calculate_uptime_cpu_memory(config)
        }
        
        logger.info(f"Анализ конфигурации {config['hostname']} завершен")
        return report
    
    # Генерация отчета по всем конфигурациям
    def generate_report(self, output_file: str = "analysis_report.json") -> None:
        """
        Генерирует аналитический отчет по всем задачам в формате JSON.
        """
        all_reports = []
        total_configs = len(self._configs)
        
        logger.info(f"Начата генерация отчета для {total_configs} конфигураций")
        print(f"\n !!!Генерация отчета для {total_configs} конфигураций...!!!")
        
        for i, config in enumerate(self.read_configs_generator(), 1):
            report = self.analyze_all(config)
            all_reports.append(report)
            
            if i % 100 == 0:
                print(f"  Обработано {i}/{total_configs} конфигураций")
        
        # Агрегированная статистика
        aggregated = self._aggregate_reports(all_reports)
        
        final_report = {
            'metadata': {
                'total_configs': total_configs,
                'generated_at': datetime.now().isoformat(),
                'report_version': '1.0'
            },
            'individual_reports': all_reports,
            'aggregated_statistics': aggregated
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Отчет сохранен в файл {output_file}")
        print(f"Отчет сохранен в файл '{output_file}'")
    
    def _aggregate_reports(self, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Агрегирует статистику из всех отчетов.
        """
        total_traffic = sum(r['traffic_stats']['total_traffic_mb'] for r in reports)
        avg_cpu = sum(r['system_stats']['cpu_usage'] for r in reports) / len(reports)
        avg_memory = sum(r['system_stats']['memory_usage'] for r in reports) / len(reports)
        
        vulnerabilities_fixed = sum(1 for r in reports 
                                  if r['modifications']['snmp_vulnerability_fixed'])
        
        return {
            'total_traffic_mb': total_traffic,
            'average_cpu_usage': round(avg_cpu, 2),
            'average_memory_usage': round(avg_memory, 2),
            'snmp_vulnerabilities_fixed': vulnerabilities_fixed,
            'average_uptime_days': round(sum(r['system_stats']['uptime_days'] 
                                       for r in reports) / len(reports), 2)
        }
    
    # Методы сериализации
    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует полное состояние объекта в словарь.
        """
        return {
            'file_path': self._file_path,
            'configs_count': len(self._configs),
            'configs_sample': self._configs[:5] if self._configs else []
        }
    
    def from_dict(self, state: Dict[str, Any]) -> None:
        """
        Восстанавливает состояние объекта из словаря.
        """
        self._file_path = state.get('file_path', 'router_configs.json')
        self._load_configs()
        logger.info("Состояние объекта восстановлено из словаря")
        print("✅ Состояние объекта восстановлено")
    
    def save_state(self, file_path: str = "manager_state.json") -> None:
        """
        Сохраняет полное состояние объекта в JSON файл.
        """
        state = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        logger.info(f"Состояние сохранено в {file_path}")
        print(f"✅ Состояние сохранено в '{file_path}'")
    
    def load_state(self, file_path: str = "manager_state.json") -> None:
        """
        Загружает состояние объекта из JSON файла.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        self.from_dict(state)
        logger.info(f"Состояние загружено из {file_path}")
        print(f"✅ Состояние загружено из '{file_path}'")