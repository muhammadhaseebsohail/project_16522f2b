import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import axios from 'axios';
import AuthComponent from './AuthComponent';

jest.mock('axios');

describe('AuthComponent', () => {
  let apiUrl;

  beforeEach(() => {
    apiUrl = 'http://dummyapi.com';
  });

  it('should render without crashing', () => {
    render(<AuthComponent apiUrl={apiUrl} />);
  });

  it('should display error when no apiUrl is provided', () => {
    console.error = jest.fn();
    render(<AuthComponent />);
    expect(console.error).toHaveBeenCalled();
  });

  it('should update state when input values change', () => {
    render(<AuthComponent apiUrl={apiUrl} />);
    fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'username' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password' } });
    expect(screen.getByPlaceholderText('Username')).toHaveValue('username');
    expect(screen.getByPlaceholderText('Password')).toHaveValue('password');
  });

  it('should display loading state when form is submitted', async () => {
    axios.post.mockResolvedValueOnce({ status: 200 });
    render(<AuthComponent apiUrl={apiUrl} />);
    fireEvent.click(screen.getByText('Submit'));
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display error state when api call fails', async () => {
    axios.post.mockRejectedValueOnce(new Error());
    render(<AuthComponent apiUrl={apiUrl} />);
    fireEvent.click(screen.getByText('Submit'));
    await waitFor(() => expect(screen.getByText('An error occurred')).toBeInTheDocument());
  });

  it('should display authentication error when response status is not 200', async () => {
    axios.post.mockResolvedValueOnce({ status: 401 });
    render(<AuthComponent apiUrl={apiUrl} />);
    fireEvent.click(screen.getByText('Submit'));
    await waitFor(() => expect(screen.getByText('Authentication failed')).toBeInTheDocument());
  });

  it('should pass a11y check', async () => {
    const { container } = render(<AuthComponent apiUrl={apiUrl} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});