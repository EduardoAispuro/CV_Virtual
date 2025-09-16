import React, { useState } from 'react'
import axios from 'axios'
import { Shield, Search, AlertTriangle, CheckCircle, XCircle, Filter } from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000'

const NmapScanner = () => {
  const [portRange, setPortRange] = useState('22-443')
  const [target] = useState('localhost') // Fixed to localhost for security
  const [scanning, setScanning] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleScan = async () => {
    if (!portRange.trim()) {
      setError('Por favor ingrese un rango de puertos válido')
      return
    }

    // Validate port range format
    const portRangeRegex = /^\d+-\d+$/
    if (!portRangeRegex.test(portRange.trim())) {
      setError('Formato inválido. Use formato: "22-443"')
      return
    }

    try {
      setScanning(true)
      setError(null)
      setResults(null)

      const response = await axios.post(`${API_BASE_URL}/api/scan`, {
        port_range: portRange.trim(),
        target: target
      })

      setResults(response.data)
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error)
      } else {
        setError('Error al realizar el escaneo. Verifique que el servidor backend esté ejecutándose.')
      }
      console.error('Scan error:', err)
    } finally {
      setScanning(false)
    }
  }

  const getPortStatusIcon = (status) => {
    switch (status) {
      case 'open':
        return <CheckCircle size={16} className="text-green-600" />
      case 'closed':
        return <XCircle size={16} className="text-red-600" />
      case 'filtered':
        return <Filter size={16} className="text-yellow-600" />
      default:
        return <AlertTriangle size={16} className="text-gray-600" />
    }
  }

  const renderPortList = (ports, title, statusClass) => {
    if (!ports || ports.length === 0) return null

    return (
      <div style={{ marginBottom: '1.5rem' }}>
        <h4 style={{ 
          fontSize: '1.1rem', 
          fontWeight: '600', 
          marginBottom: '1rem',
          color: 'var(--text-dark)'
        }}>
          {title} ({ports.length})
        </h4>
        <div className="port-list">
          {ports.map((port, index) => (
            <div key={index} className="port-item">
              <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                Puerto {port.port}/{port.protocol}
                <span className={`port-status ${statusClass}`}>
                  {port.state}
                </span>
              </h4>
              <div className="port-details">
                <p><strong>Servicio:</strong> {port.name || 'Desconocido'}</p>
                {port.product && <p><strong>Producto:</strong> {port.product}</p>}
                {port.version && <p><strong>Versión:</strong> {port.version}</p>}
                {port.extrainfo && <p><strong>Info adicional:</strong> {port.extrainfo}</p>}
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div>
      <h3 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Shield size={24} />
        Escáner de Puertos (nmap)
      </h3>
      
      <div style={{ marginBottom: '1rem' }}>
        <p style={{ color: 'var(--text-light)', marginBottom: '1rem' }}>
          Herramienta de seguridad para escanear puertos abiertos en localhost usando nmap.
        </p>
        
        <div className="alert alert-warning" style={{ fontSize: '0.9rem' }}>
          <AlertTriangle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
          <strong>Nota de Seguridad:</strong> Solo se permite escanear localhost (127.0.0.1) por razones de seguridad.
        </div>
      </div>

      <div className="input-group">
        <label htmlFor="portRange">Rango de Puertos:</label>
        <input
          id="portRange"
          type="text"
          value={portRange}
          onChange={(e) => setPortRange(e.target.value)}
          placeholder="Ej: 22-443, 80-8080"
          disabled={scanning}
        />
        <small style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>
          Formato: puerto_inicio-puerto_fin (máximo 1000 puertos)
        </small>
      </div>

      <div className="input-group">
        <label>Objetivo:</label>
        <input
          type="text"
          value={target}
          disabled
          style={{ backgroundColor: 'var(--bg-gray)', cursor: 'not-allowed' }}
        />
        <small style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>
          Fijo en localhost por seguridad
        </small>
      </div>

      <button
        className="btn btn-primary"
        onClick={handleScan}
        disabled={scanning}
        style={{ width: '100%' }}
      >
        {scanning ? (
          <>
            <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
            Escaneando...
          </>
        ) : (
          <>
            <Search size={16} />
            Iniciar Escaneo
          </>
        )}
      </button>

      {error && (
        <div className="alert alert-error" style={{ marginTop: '1rem' }}>
          <AlertTriangle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
          {error}
        </div>
      )}

      {results && (
        <div className="scan-results">
          <h4 style={{ 
            fontSize: '1.2rem', 
            fontWeight: '600', 
            marginBottom: '1rem',
            color: 'var(--primary-color)'
          }}>
            Resultados del Escaneo
          </h4>
          
          <div style={{ 
            background: 'var(--bg-gray)', 
            padding: '1rem', 
            borderRadius: '8px',
            marginBottom: '1.5rem'
          }}>
            <p><strong>Objetivo:</strong> {results.target}</p>
            <p><strong>Rango:</strong> {results.port_range}</p>
            <p><strong>Timestamp:</strong> {results.timestamp}</p>
            {results.summary && (
              <div style={{ marginTop: '0.5rem' }}>
                <p><strong>Resumen:</strong></p>
                <ul style={{ marginLeft: '1rem', marginTop: '0.5rem' }}>
                  <li>Total de puertos escaneados: {results.summary.total_ports_scanned}</li>
                  <li style={{ color: 'var(--success-color)' }}>
                    Puertos abiertos: {results.summary.open_ports_count}
                  </li>
                  <li style={{ color: 'var(--error-color)' }}>
                    Puertos cerrados: {results.summary.closed_ports_count}
                  </li>
                  <li style={{ color: 'var(--warning-color)' }}>
                    Puertos filtrados: {results.summary.filtered_ports_count}
                  </li>
                </ul>
              </div>
            )}
          </div>

          {results.error ? (
            <div className="alert alert-error">
              <AlertTriangle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
              Error en el escaneo: {results.error}
            </div>
          ) : (
            <div>
              {renderPortList(results.results?.open_ports, 'Puertos Abiertos', 'open')}
              {renderPortList(results.results?.closed_ports, 'Puertos Cerrados', 'closed')}
              {renderPortList(results.results?.filtered_ports, 'Puertos Filtrados', 'filtered')}
              
              {(!results.results?.open_ports?.length && 
                !results.results?.closed_ports?.length && 
                !results.results?.filtered_ports?.length) && (
                <div className="alert alert-warning">
                  No se encontraron puertos en el rango especificado.
                </div>
              )}
            </div>
          )}

          {results.results?.host_info && (
            <div style={{ 
              background: 'var(--bg-gray)', 
              padding: '1rem', 
              borderRadius: '8px',
              marginTop: '1rem'
            }}>
              <h5 style={{ marginBottom: '0.5rem' }}>Información del Host:</h5>
              <p><strong>Estado:</strong> {results.results.host_info.state}</p>
              <p><strong>Hostname:</strong> {results.results.host_info.hostname || 'N/A'}</p>
              {results.results.host_info.os_matches && results.results.host_info.os_matches.length > 0 && (
                <div>
                  <p><strong>Sistema Operativo Detectado:</strong></p>
                  <ul style={{ marginLeft: '1rem' }}>
                    {results.results.host_info.os_matches.slice(0, 3).map((os, index) => (
                      <li key={index}>
                        {os.name} (Precisión: {os.accuracy}%)
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default NmapScanner
