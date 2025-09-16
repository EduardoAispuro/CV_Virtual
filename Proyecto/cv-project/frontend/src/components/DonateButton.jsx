import React, { useState } from 'react'
import axios from 'axios'
import { Heart, CreditCard, DollarSign, AlertTriangle, ExternalLink } from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000'

const DonateButton = () => {
  const [amount, setAmount] = useState(500) // Default $5.00 in cents
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const predefinedAmounts = [
    { value: 300, label: '$3.00' },
    { value: 500, label: '$5.00' },
    { value: 1000, label: '$10.00' },
    { value: 2000, label: '$20.00' }
  ]

  const handleDonate = async () => {
    if (amount < 50) {
      setError('El monto mínimo es $0.50 USD')
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await axios.post(`${API_BASE_URL}/api/create-checkout-session`, {
        amount: amount
      })

      if (response.data.checkout_url) {
        // Redirect to Stripe Checkout
        window.open(response.data.checkout_url, '_blank')
      } else {
        setError('No se pudo crear la sesión de pago')
      }
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error)
      } else {
        setError('Error al crear la sesión de pago. Verifique que el servidor backend esté ejecutándose.')
      }
      console.error('Payment error:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (cents) => {
    return `$${(cents / 100).toFixed(2)} USD`
  }

  return (
    <div>
      <h3 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Heart size={24} />
        Apoyo al Proyecto
      </h3>
      
      <div style={{ marginBottom: '1.5rem' }}>
        <p style={{ color: 'var(--text-light)', marginBottom: '1rem' }}>
          Si te gusta este proyecto y quieres apoyar su desarrollo, puedes hacer una donación usando Stripe.
        </p>
        
        <div className="alert alert-warning" style={{ fontSize: '0.9rem' }}>
          <AlertTriangle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
          <strong>Modo de Prueba:</strong> Usa la tarjeta de prueba 4242 4242 4242 4242 para probar el sistema.
        </div>
      </div>

      <div className="input-group">
        <label>Seleccionar Monto:</label>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', 
          gap: '0.5rem',
          marginBottom: '1rem'
        }}>
          {predefinedAmounts.map((preset) => (
            <button
              key={preset.value}
              className={`btn ${amount === preset.value ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setAmount(preset.value)}
              disabled={loading}
              style={{ fontSize: '0.9rem', padding: '0.5rem' }}
            >
              {preset.label}
            </button>
          ))}
        </div>
      </div>

      <div className="input-group">
        <label htmlFor="customAmount">Monto Personalizado (USD):</label>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <DollarSign size={20} style={{ color: 'var(--text-light)' }} />
          <input
            id="customAmount"
            type="number"
            min="0.50"
            step="0.50"
            value={(amount / 100).toFixed(2)}
            onChange={(e) => setAmount(Math.round(parseFloat(e.target.value || 0) * 100))}
            placeholder="5.00"
            disabled={loading}
            style={{ flex: 1 }}
          />
        </div>
        <small style={{ color: 'var(--text-light)', fontSize: '0.9rem' }}>
          Monto mínimo: $0.50 USD
        </small>
      </div>

      <div style={{ 
        background: 'var(--bg-gray)', 
        padding: '1rem', 
        borderRadius: '8px',
        marginBottom: '1rem'
      }}>
        <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-dark)' }}>
          Resumen de Donación:
        </h4>
        <p style={{ fontSize: '1.1rem', fontWeight: '600', color: 'var(--primary-color)' }}>
          Total: {formatCurrency(amount)}
        </p>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-light)' }}>
          Procesado por Stripe (modo de prueba)
        </p>
      </div>

      <button
        className="btn btn-primary"
        onClick={handleDonate}
        disabled={loading || amount < 50}
        style={{ width: '100%', marginBottom: '1rem' }}
      >
        {loading ? (
          <>
            <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
            Procesando...
          </>
        ) : (
          <>
            <CreditCard size={16} />
            Donar {formatCurrency(amount)}
            <ExternalLink size={14} />
          </>
        )}
      </button>

      {error && (
        <div className="alert alert-error">
          <AlertTriangle size={16} style={{ display: 'inline', marginRight: '0.5rem' }} />
          {error}
        </div>
      )}

      <div style={{ 
        fontSize: '0.8rem', 
        color: 'var(--text-light)', 
        textAlign: 'center',
        marginTop: '1rem'
      }}>
        <p><strong>Tarjetas de Prueba Stripe:</strong></p>
        <ul style={{ listStyle: 'none', padding: 0, marginTop: '0.5rem' }}>
          <li>• Visa: 4242 4242 4242 4242</li>
          <li>• Visa (debit): 4000 0566 5566 5556</li>
          <li>• Mastercard: 5555 5555 5555 4444</li>
          <li>• American Express: 3782 822463 10005</li>
        </ul>
        <p style={{ marginTop: '0.5rem' }}>
          Usar cualquier fecha futura para expiración y cualquier CVC de 3-4 dígitos.
        </p>
      </div>

      <div style={{ 
        background: 'var(--bg-gray)', 
        padding: '1rem', 
        borderRadius: '8px',
        marginTop: '1rem',
        fontSize: '0.9rem'
      }}>
        <h5 style={{ marginBottom: '0.5rem', color: 'var(--text-dark)' }}>
          ¿Cómo funciona?
        </h5>
        <ol style={{ marginLeft: '1rem', color: 'var(--text-light)' }}>
          <li>Selecciona o ingresa el monto que deseas donar</li>
          <li>Haz clic en "Donar" para crear una sesión de pago</li>
          <li>Serás redirigido a Stripe Checkout en una nueva pestaña</li>
          <li>Completa el pago usando una tarjeta de prueba</li>
          <li>¡Gracias por tu apoyo al proyecto!</li>
        </ol>
      </div>
    </div>
  )
}

export default DonateButton
