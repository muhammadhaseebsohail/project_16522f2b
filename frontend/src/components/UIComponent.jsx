import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import styles from './UIComponents.module.css';

const UIComponent = ({ url }) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get(url);
        setData(response.data);
      } catch (error) {
        setError(error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [url]);

  if (isLoading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return (
      <div className={styles.error}>An error occurred: {error.message}</div>
    );
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>UI Component</h1>
      <div className={styles.content}>{data && data.map((item, index) => (
        <div key={index} className={styles.item}>{item}</div>
      ))}</div>
    </div>
  );
};

UIComponent.propTypes = {
  url: PropTypes.string.isRequired,
};

export default UIComponent;