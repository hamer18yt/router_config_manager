 
"""
Модуль генерации тестовых данных для конфигурации сетевых устройств.
Использует библиотеку Faker для создания реалистичных данных.
"""

import json
import random
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from faker import Faker

fake = Faker()

"""
ПРОМПТ ДЛЯ НЕЙРОСЕТИ:
=====================
Сгенерируй 1000 конфигураций сетевых маршрутизаторов в формате JSON.

Использованный AI: ChatGPT-4
Параметры доступа: API ключ не требуется
Дата генерации: 2026-06-07
"""

def generate_interface_name() -> str:
    """Генерирует случайное имя интерфейса."""
    types = ["GigabitEthernet", "FastEthernet", "Ethernet"]
    type_choice = random.choice(types)
    
    if type_choice == "GigabitEthernet":
        return f"{type_choice}{random.randint(0, 3)}/{random.randint(0, 3)}"
    elif type_choice == "FastEthernet":
        return f"{type_choice}{random.randint(0, 3)}/{random.randint(0, 3)}"
    else:
        return f"{type_choice}{random.randint(0, 3)}"

def generate_interface() -> Dict[str, Any]:
    """Генерирует конфигурацию одного интерфейса."""
    acl_options = ["ALLOW_HTTP", "ALLOW_SSH", "DENY_ALL", None]
    weights = [0.3, 0.3, 0.1, 0.3]
    
    return {
        "ip": fake.ipv4(),
        "status": random.choice(["up", "down"]),
        "acl_in": random.choices(acl_options, weights=weights)[0],
        "traffic_in_mb": random.randint(0, 5000),
        "traffic_out_mb": random.randint(0, 5000)
    }

def generate_static_route() -> Dict[str, Any]:
    """Генерирует один статический маршрут."""
    return {
        "destination": f"{fake.ipv4()}/{random.randint(8, 30)}",
        "next_hop": fake.ipv4(),
        "metric": random.randint(1, 10)
    }

def generate_router_config() -> Dict[str, Any]:
    """Генерирует полную конфигурацию маршрутизатора."""
    num_interfaces = random.randint(5, 12)
    interfaces = {}
    
    for _ in range(num_interfaces):
        interfaces[generate_interface_name()] = generate_interface()
    
    static_routes = [generate_static_route() for _ in range(random.randint(3, 8))]
    dynamic_routes = random.randint(50, 200)
    total_routes = dynamic_routes + len(static_routes)
    
    # В 10% случаев создаем несоответствие
    if random.random() < 0.1:
        total_routes = dynamic_routes + len(static_routes) + random.randint(-3, 3)
    
    num_blocked_ips = random.randint(5, 20)
    blocked_ips = [fake.ipv4() for _ in range(num_blocked_ips)]
    
    return {
        "hostname": f"Router-{fake.city()}-{random.randint(1, 999)}",
        "interfaces": interfaces,
        "routing": {
            "static": static_routes,
            "dynamic_routes": dynamic_routes,
            "total_routes": total_routes
        },
        "snmp": {
            "community": random.choice(["public", "private", "secure_comms"]),
            "access": random.choice(["read-only", "read-write"])
        },
        "security": {
            "failed_logins": random.randint(0, 150),
            "last_attack_timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "blocked_ips": blocked_ips
        },
        "uptime_seconds": random.randint(86400, 2592000),
        "cpu_usage": round(random.uniform(0, 100), 1),
        "memory_usage": round(random.uniform(0, 100), 1)
    }

def generate_configs(num_configs: int = 1000, output_file: str = "router_configs.json"):
    """
    Генерирует указанное количество конфигураций и сохраняет в JSON файл.
    
    Args:
        num_configs: Количество генерируемых конфигураций
        output_file: Имя выходного файла
    """
    print(f"Начало генерации {num_configs} конфигураций...")
    configs = []
    
    for i in range(num_configs):
        config = generate_router_config()
        configs.append(config)
        
        if (i + 1) % 100 == 0:
            print(f"Сгенерировано {i + 1} конфигураций...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)
    
    print(f"Генерация завершена! Сохранено {num_configs} конфигураций в файл '{output_file}'")
    print(f"Размер файла: {round(os.path.getsize(output_file) / 1024 / 1024, 2)} MB")

if __name__ == "__main__":
    generate_configs(1000)