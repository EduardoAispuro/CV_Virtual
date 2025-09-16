import nmap
from datetime import datetime
import socket

def scan_ports(target, port_range):
    """
    Escanea puertos usando nmap en el objetivo especificado
    
    Args:
        target (str): Dirección IP o hostname a escanear (solo localhost/127.0.0.1)
        port_range (str): Rango de puertos en formato "inicio-fin" (ej: "22-443")
    
    Returns:
        dict: Resultados del escaneo con información de puertos
    """
    try:
        # Inicializar el escáner nmap
        nm = nmap.PortScanner()
        
        # Realizar el escaneo
        print(f"🔍 Escaneando {target} en rango de puertos {port_range}...")
        scan_result = nm.scan(target, port_range, arguments='-sS -O -A')
        
        # Procesar resultados
        results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target': target,
            'port_range': port_range,
            'scan_info': {},
            'host_info': {},
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': []
        }
        
        # Información general del escaneo
        if 'nmap' in scan_result:
            results['scan_info'] = {
                'command_line': scan_result['nmap']['command_line'],
                'scanstats': scan_result['nmap']['scanstats']
            }
        
        # Procesar información del host
        for host in nm.all_hosts():
            host_info = {
                'hostname': nm[host].hostname(),
                'state': nm[host].state(),
                'protocols': list(nm[host].all_protocols())
            }
            
            # Obtener información del OS si está disponible
            if 'osmatch' in nm[host]:
                os_matches = []
                for osmatch in nm[host]['osmatch']:
                    os_matches.append({
                        'name': osmatch['name'],
                        'accuracy': osmatch['accuracy']
                    })
                host_info['os_matches'] = os_matches
            
            results['host_info'] = host_info
            
            # Procesar puertos para cada protocolo
            for protocol in nm[host].all_protocols():
                ports = nm[host][protocol].keys()
                
                for port in ports:
                    port_info = {
                        'port': port,
                        'protocol': protocol,
                        'state': nm[host][protocol][port]['state'],
                        'name': nm[host][protocol][port]['name'],
                        'product': nm[host][protocol][port].get('product', ''),
                        'version': nm[host][protocol][port].get('version', ''),
                        'extrainfo': nm[host][protocol][port].get('extrainfo', '')
                    }
                    
                    # Clasificar puertos por estado
                    if port_info['state'] == 'open':
                        results['open_ports'].append(port_info)
                    elif port_info['state'] == 'closed':
                        results['closed_ports'].append(port_info)
                    elif port_info['state'] == 'filtered':
                        results['filtered_ports'].append(port_info)
        
        # Agregar resumen
        results['summary'] = {
            'total_ports_scanned': len(results['open_ports']) + len(results['closed_ports']) + len(results['filtered_ports']),
            'open_ports_count': len(results['open_ports']),
            'closed_ports_count': len(results['closed_ports']),
            'filtered_ports_count': len(results['filtered_ports'])
        }
        
        print(f"✅ Escaneo completado. Puertos abiertos: {len(results['open_ports'])}")
        return results
        
    except nmap.PortScannerError as e:
        error_msg = f"Error de nmap: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'error': error_msg,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target': target,
            'port_range': port_range
        }
    
    except Exception as e:
        error_msg = f"Error inesperado durante el escaneo: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            'error': error_msg,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target': target,
            'port_range': port_range
        }

def check_single_port(host, port, timeout=3):
    """
    Verifica si un puerto específico está abierto usando socket
    
    Args:
        host (str): Dirección del host
        port (int): Puerto a verificar
        timeout (int): Timeout en segundos
    
    Returns:
        bool: True si el puerto está abierto, False en caso contrario
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def get_common_ports():
    """
    Retorna una lista de puertos comunes con sus servicios asociados
    
    Returns:
        dict: Diccionario con puertos comunes y sus servicios
    """
    return {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        3389: "RDP",
        5432: "PostgreSQL",
        3306: "MySQL",
        27017: "MongoDB",
        6379: "Redis",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
        9200: "Elasticsearch",
        5000: "Flask Dev Server",
        3000: "Node.js Dev Server",
        5173: "Vite Dev Server"
    }

def validate_port_range(port_range):
    """
    Valida que el rango de puertos tenga el formato correcto
    
    Args:
        port_range (str): Rango en formato "inicio-fin"
    
    Returns:
        tuple: (bool, str) - (es_válido, mensaje_error)
    """
    try:
        if '-' not in port_range:
            return False, "El rango debe tener formato 'inicio-fin' (ej: '22-443')"
        
        start_port, end_port = map(int, port_range.split('-'))
        
        if start_port < 1 or end_port > 65535:
            return False, "Los puertos deben estar entre 1 y 65535"
        
        if start_port > end_port:
            return False, "El puerto inicial debe ser menor o igual al puerto final"
        
        if end_port - start_port > 1000:
            return False, "El rango no puede ser mayor a 1000 puertos para evitar escaneos muy largos"
        
        return True, "Rango válido"
        
    except ValueError:
        return False, "El rango debe contener solo números enteros"
