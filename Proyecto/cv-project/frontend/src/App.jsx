import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, useInView } from 'framer-motion';
import { User, Mail, Phone, MapPin, Briefcase, GraduationCap, Code, Award, Calendar, Building, Camera } from 'lucide-react';
import Typed from 'typed.js';
import AOS from 'aos';
import NmapScanner from './components/NmapScanner';
import DonateButton from './components/DonateButton';
import './index.css';

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [cvData, setCvData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isResetting, setIsResetting] = useState(false)
  const titleRef = useRef(null)

  useEffect(() => {
    fetchData();
    AOS.init({
      duration: 1000,
      easing: 'ease-out-cubic',
      once: true,
      offset: 100
    });
  }, []);

  useEffect(() => {
    if (cvData && titleRef.current) {
      const typed = new Typed(titleRef.current, {
        strings: [
          cvData.profile.title,
          'Backend Developer',
          'Software Engineer',
          'Full Stack Developer'
        ],
        typeSpeed: 50,
        backSpeed: 30,
        backDelay: 2000,
        loop: true,
        showCursor: true,
        cursorChar: '|'
      })
      
      return () => typed.destroy()
    }
  }, [cvData])

  const handleResetData = async () => {
    setIsResetting(true);
    setError(null);
    try {
      const resetResponse = await axios.post(`${API_BASE_URL}/api/reset-data`);
      if (resetResponse.data.status === 'success') {
        fetchData(); // Vuelve a cargar los datos después de resetear
      } else {
        throw new Error(resetResponse.data.error || 'Error al resetear los datos.');
      }
    } catch (err) {
      const errorMessage = err.response ? `${err.response.status} ${err.response.statusText}: ${err.response.data.error}` : err.message;
      setError(`Error al resetear los datos: ${errorMessage}`);
      console.error("Error resetting data:", err);
    } finally {
      setIsResetting(false);
    }
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/cv`);
      setCvData(response.data);
      setError(null);
    } catch (err) {
      const errorMessage = err.response ? `${err.response.status} ${err.response.statusText}: ${err.response.data.error}` : err.message;
      setError(`No se pudieron cargar los datos del CV: ${errorMessage}`);
      console.error('Error fetching CV data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('photo', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload-photo`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      if (response.data.status === 'success') {
        // Optimistically update the UI
        setCvData(prevData => ({
          ...prevData,
          profile: { ...prevData.profile, photo_url: response.data.photo_url }
        }));
      } else {
        throw new Error(response.data.error || 'Failed to upload photo.');
      }
    } catch (err) {
      const errorMessage = err.response ? `${err.response.status} ${err.response.statusText}: ${err.response.data.error}` : err.message;
      setError(`Error al subir la foto: ${errorMessage}`);
      console.error('Error uploading photo:', err);
    }
  };

  const AnimatedSection = ({ children, className = '', delay = 0 }) => {
    const ref = useRef(null)
    const isInView = useInView(ref, { once: true, margin: '-100px' })
    
    return (
      <motion.div
        ref={ref}
        initial={{ opacity: 0, y: 50 }}
        animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
        transition={{ duration: 0.6, delay, ease: 'easeOut' }}
        className={className}
      >
        {children}
      </motion.div>
    )
  }

  const CodingSkillTag = ({ skill, index }) => {
    const programmingLanguages = ['Java', 'React', 'Node.js', 'C#', 'Python']
    const isCoding = programmingLanguages.includes(skill)
    
    return (
      <motion.span
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3, delay: index * 0.1 }}
        whileHover={{ scale: 1.05, y: -2 }}
        className={`skill-tag ${isCoding ? 'coding-animation' : ''}`}
      >
        {skill}
      </motion.span>
    )
  }

  if (loading) {
    return <div className="loading-container"><div className="loader"></div><p>Cargando CV...</p></div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2><i className="fas fa-exclamation-triangle"></i> Error al Cargar</h2>
        <p>{error}</p>
        <div className="error-actions">
          <button onClick={() => fetchData()} className="retry-button">Reintentar</button>
          <button onClick={handleResetData} disabled={isResetting} className="reset-button">
            {isResetting ? 'Reseteando...' : 'Forzar Actualización de Datos'}
          </button>
        </div>
      </div>
    );
  }

  if (!cvData) {
    return <div className="loading-container"><p>No se encontraron datos del CV.</p></div>;
  }

  return (
    <div className="container">
      <div className="fixed-controls">
        <button onClick={handleResetData} disabled={isResetting} className="reset-button-main" title="Forzar actualización de datos desde el servidor">
          {isResetting ? <div className="loader-small"></div> : <i className="fas fa-sync-alt"></i>}
        </button>
      </div>

      {/* Header */}
      <motion.div 
        className="header"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: 'easeOut' }}
      >
        <motion.h1
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {cvData.profile.name}
        </motion.h1>
        <div className="title typing-animation">
          <span ref={titleRef}></span>
        </div>
      </motion.div>

      {/* Profile Section */}
      <AnimatedSection className="card" delay={0.3}>
        <div className="profile-section">
          <motion.div 
            className="profile-photo-container"
            whileHover={{ scale: 1.05 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            {cvData.profile.photo_url ? (
              <img src={cvData.profile.photo_url} alt="Profile" className="profile-photo" />
            ) : (
              <div className="profile-photo-placeholder">
                <User size={80} />
              </div>
            )}
            <input
              type="file"
              accept="image/*"
              onChange={handlePhotoUpload}
              style={{ display: 'none' }}
              id="photo-upload"
            />
            <label htmlFor="photo-upload" className="upload-photo-btn">
              <Camera size={20} />
            </label>
          </motion.div>
          
          <div className="profile-info">
            <motion.h2
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              {cvData.profile.name}
            </motion.h2>
            
            <motion.div 
              className="contact-info"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <motion.div 
                className="contact-item"
                whileHover={{ x: 5 }}
                transition={{ type: 'spring', stiffness: 400 }}
              >
                <Mail className="icon" size={20} />
                <span>{cvData.profile.email}</span>
              </motion.div>
              <motion.div 
                className="contact-item"
                whileHover={{ x: 5 }}
                transition={{ type: 'spring', stiffness: 400 }}
              >
                <Phone className="icon" size={20} />
                <span>{cvData.profile.phone}</span>
              </motion.div>
              <motion.div 
                className="contact-item"
                whileHover={{ x: 5 }}
                transition={{ type: 'spring', stiffness: 400 }}
              >
                <MapPin className="icon" size={20} />
                <span>{cvData.profile.location}</span>
              </motion.div>
            </motion.div>
            
            <motion.div 
              className="summary"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
            >
              <p>{cvData.profile.summary}</p>
            </motion.div>
          </div>
        </div>
      </AnimatedSection>

      {/* Experience Section */}
      <AnimatedSection className="card" delay={0.4}>
        <motion.h2 
          className="section-title"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <Briefcase className="icon" size={24} />
          Experiencia Profesional
        </motion.h2>
        {cvData.experiences && cvData.experiences.map((exp, index) => (
          <motion.div 
            key={index} 
            className="experience-item"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.5 + index * 0.1 }}
            whileHover={{ y: -4 }}
          >
            <h3>{exp.position}</h3>
            <p className="company">
              <Building className="icon" size={16} />
              {exp.company}
            </p>
            <p className="period">
              <Calendar className="icon" size={16} />
              {exp.period}
            </p>
            <p className="location">
              <MapPin className="icon" size={16} />
              {exp.location}
            </p>
            <ul className="responsibilities">
              {exp.responsibilities && exp.responsibilities.map((resp, respIndex) => (
                <motion.li 
                  key={respIndex}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.6 + respIndex * 0.1 }}
                  whileHover={{ x: 5 }}
                >
                  {resp}
                </motion.li>
              ))}
            </ul>
          </motion.div>
        ))}
      </AnimatedSection>

      {/* Education Section */}
      <AnimatedSection className="card" delay={0.5}>
        <motion.h2 
          className="section-title"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <GraduationCap className="icon" size={24} />
          Educación
        </motion.h2>
        {cvData.education && cvData.education.map((edu, index) => (
          <motion.div 
            key={index} 
            className="education-item"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
            whileHover={{ y: -4 }}
          >
            <h3>{edu.degree}</h3>
            <p className="institution">
              <Building className="icon" size={16} />
              {edu.institution}
            </p>
            <p className="period">
              <Calendar className="icon" size={16} />
              {edu.period}
            </p>
            <p className="location">
              <MapPin className="icon" size={16} />
              {edu.location}
            </p>
          </motion.div>
        ))}
      </AnimatedSection>

      {/* Skills Section */}
      <AnimatedSection className="card" delay={0.6}>
        <motion.h2 
          className="section-title"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <Code className="icon" size={24} />
          Habilidades Técnicas
        </motion.h2>
        <div className="skills-grid">
          {cvData.skills && Object.entries(cvData.skills).map(([category, skillsList], index) => (
            <motion.div 
              key={index} 
              className="skill-category"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.7 + index * 0.1 }}
              whileHover={{ y: -8 }}
            >
              <h4>{category.replace('_', ' ').toUpperCase()}</h4>
              <div className="skill-tags">
                {skillsList && skillsList.map((skill, skillIndex) => (
                  <CodingSkillTag key={skillIndex} skill={skill} index={skillIndex} />
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </AnimatedSection>

      {/* Tools Section */}
      <AnimatedSection className="card" delay={0.7}>
        <motion.h2 
          className="section-title"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <Award className="icon" size={24} />
          Herramientas Adicionales
        </motion.h2>
        <div className="tools-section">
          <motion.div 
            className="tool-card"
            whileHover={{ scale: 1.02, y: -5 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            <h3>Port Scanner</h3>
            <p>Herramienta de escaneo de puertos con nmap</p>
            <NmapScanner />
          </motion.div>
          <motion.div 
            className="tool-card"
            whileHover={{ scale: 1.02, y: -5 }}
            transition={{ type: 'spring', stiffness: 300 }}
          >
            <h3>Donaciones</h3>
            <p>Apoya el desarrollo de este proyecto</p>
            <DonateButton />
          </motion.div>
        </div>
      </AnimatedSection>
    </div>
  )
}

export default App
