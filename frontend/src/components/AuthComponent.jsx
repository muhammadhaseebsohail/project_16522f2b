import React, { useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import styled from 'styled-components';

const FormWrapper = styled.div`
  display: flex;
  flex-direction: column;
  width: 300px;
`;

const Input = styled.input`
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
`;

const Button = styled.button`
  padding: 10px;
  background-color: blue;
  color: white;
  cursor: pointer;
`;

const ErrorMessage = styled.p`
  color: red;
`;

const LoadingMessage = styled.p`
  color: green;
`;

function AuthComponent({apiUrl}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUsernameChange = (event) => setUsername(event.target.value);
  const handlePasswordChange = (event) => setPassword(event.target.value);

  const handleSubmit = async (event) => {
    event.preventDefault();

    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post(apiUrl, {
        username,
        password,
      });

      setIsLoading(false);

      if (response.status === 200) {
        // Handle successful authentication here
      } else {
        setError('Authentication failed');
      }
    } catch (error) {
      setIsLoading(false);
      setError('An error occurred');
    }
  };

  return (
    <FormWrapper>
      <Input type="text" value={username} onChange={handleUsernameChange} placeholder="Username" />
      <Input type="password" value={password} onChange={handlePasswordChange} placeholder="Password" />
      <Button onClick={handleSubmit}>Submit</Button>
      {isLoading && <LoadingMessage>Loading...</LoadingMessage>}
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </FormWrapper>
  );
}

AuthComponent.propTypes = {
  apiUrl: PropTypes.string.isRequired,
};

export default AuthComponent;