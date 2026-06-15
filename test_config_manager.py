"""
Модуль тестирования ConfigManager.
Содержит unit-тесты для всех публичных методов.
"""

import unittest
import json
import tempfile
import os
from config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    """Тестовый класс для ConfigManager."""
    
    def setUp(self):
        """Подготовка тестовых данных."""
        self.test_configs = [
            {
                "hostname": "TestRouter1",
                "interfaces": {
                    "GigabitEthernet0/0": {
                        "ip": "192.168.1.1",
                        "status": "up",
                        "acl_in": "ALLOW_HTTP",
                        "traffic_in_mb": 1000,
                        "traffic_out_mb": 500
                    },
                    "GigabitEthernet0/1": {
                        "ip": "10.0.0.1",
                        "status": "down",
                        "acl_in": None,
                        "traffic_in_mb": 0,
                        "traffic_out_mb": 0
                    }
                },
                "routing": {
                    "static": [
                        {"destination": "0.0.0.0/0", "next_hop": "10.0.0.254", "metric": 1},
                        {"destination": "192.168.10.0/24", "next_hop": "172.16.1.254", "metric": 2}
                    ],
                    "dynamic_routes": 100,
                    "total_routes": 102
                },
                "snmp": {"community": "public", "access": "read-only"},
                "security": {
                    "failed_logins": 10,
                    "last_attack_timestamp": "2025-06-03T08:15:00",
                    "blocked_ips": ["192.168.1.100", "10.0.0.50", "172.16.3.200"]
                },
                "uptime_seconds": 864000,
                "cpu_usage": 45.5,
                "memory_usage": 62.3
            }
        ]
        
        # Создаем временный файл с тестовыми данными
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
        json.dump(self.test_configs, self.temp_file)
        self.temp_file.close()
        
        self.manager = ConfigManager(self.temp_file.name)
    
    def tearDown(self):
        """Очистка после тестов."""
        os.unlink(self.temp_file.name)
    
    # Позитивные тесты
    def test_modify_interface_status(self):
        """Тест изменения статуса интерфейса."""
        config = self.test_configs[0].copy()
        result = self.manager.modify_interface_status(config, "GigabitEthernet0/1", "up", "10.0.0.2")
        
        self.assertTrue(result)
        self.assertEqual(config['interfaces']['GigabitEthernet0/1']['status'], 'up')
        self.assertEqual(config['interfaces']['GigabitEthernet0/1']['ip'], '10.0.0.2')
    
    def test_add_interface(self):
        """Тест добавления интерфейса."""
        config = self.test_configs[0].copy()
        result = self.manager.add_interface(config, "GigabitEthernet0/2", "192.168.2.1", "up")
        
        self.assertTrue(result)
        self.assertIn("GigabitEthernet0/2", config['interfaces'])
        self.assertEqual(config['interfaces']['GigabitEthernet0/2']['ip'], '192.168.2.1')
    
    def test_fix_snmp_vulnerability(self):
        """Тест исправления SNMP уязвимости."""
        config = self.test_configs[0].copy()
        result = self.manager.fix_snmp_vulnerability(config)
        
        self.assertTrue(result)
        self.assertEqual(config['snmp']['community'], 'private')
    
    def test_calculate_traffic_stats(self):
        """Тест расчета статистики трафика."""
        config = self.test_configs[0].copy()
        stats = self.manager.calculate_traffic_stats(config)
        
        self.assertEqual(stats['total_traffic_mb'], 1500)
        self.assertEqual(stats['total_in_mb'], 1000)
        self.assertEqual(stats['total_out_mb'], 500)
    
    def test_count_interface_status(self):
        """Тест подсчета статусов интерфейсов."""
        config = self.test_configs[0].copy()
        status = self.manager.count_interface_status(config)
        
        self.assertEqual(status['up'], 1)
        self.assertEqual(status['down'], 1)
    
    def test_analyze_acls(self):
        """Тест анализа ACL."""
        config = self.test_configs[0].copy()
        acl_stats = self.manager.analyze_acls(config)
        
        self.assertEqual(acl_stats['interfaces_with_acl'], 1)
    
    def test_calculate_routing_metrics(self):
        """Тест расчета метрик маршрутизации."""
        config = self.test_configs[0].copy()
        metrics = self.manager.calculate_routing_metrics(config)
        
        self.assertEqual(metrics['total_metric'], 3)
        self.assertEqual(metrics['average_metric'], 1.5)
    
    def test_validate_routes(self):
        """Тест валидации маршрутов."""
        config = self.test_configs[0].copy()
        is_valid, message = self.manager.validate_routes(config)
        
        self.assertTrue(is_valid)
    
    def test_analyze_blocked_ips(self):
        """Тест анализа заблокированных IP."""
        config = self.test_configs[0].copy()
        analysis = self.manager.analyze_blocked_ips(config)
        
        self.assertEqual(analysis['total_blocked_ips'], 3)
    
    def test_calculate_uptime_cpu_memory(self):
        """Тест расчета времени работы и загрузки."""
        config = self.test_configs[0].copy()
        stats = self.manager.calculate_uptime_cpu_memory(config)
        
        self.assertEqual(stats['uptime_days'], 10.0)
        self.assertEqual(stats['cpu_usage'], 45.5)
        self.assertEqual(stats['memory_usage'], 62.3)
    
    # Негативные тесты
    def test_file_not_found(self):
        """Тест обработки отсутствующего файла."""
        with self.assertRaises(FileNotFoundError):
            ConfigManager("nonexistent_file.json")
    
    def test_modify_nonexistent_interface(self):
        """Тест модификации несуществующего интерфейса."""
        config = self.test_configs[0].copy()
        result = self.manager.modify_interface_status(config, "NonexistentInterface", "up")
        
        self.assertFalse(result)
    
    def test_add_existing_interface(self):
        """Тест добавления существующего интерфейса."""
        config = self.test_configs[0].copy()
        original_count = len(config['interfaces'])
        result = self.manager.add_interface(config, "GigabitEthernet0/0", "10.0.0.2")
        
        self.assertFalse(result)
        self.assertEqual(len(config['interfaces']), original_count)
    
    def test_to_dict(self):
        """Тест сериализации в словарь."""
        state = self.manager.to_dict()
        
        self.assertIn('file_path', state)
        self.assertIn('configs_count', state)
        self.assertEqual(state['configs_count'], 1)
    
    def test_from_dict(self):
        """Тест восстановления из словаря."""
        state = self.manager.to_dict()
        new_manager = ConfigManager(self.temp_file.name)
        new_manager.from_dict(state)
        
        self.assertEqual(new_manager.configs_count, self.manager.configs_count)

if __name__ == '__main__':
    unittest.main()