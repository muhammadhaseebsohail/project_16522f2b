import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom/extend-expect';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
    let mockFetchData;

    beforeEach(() => {
        mockFetchData = jest.fn();
    });

    it('renders without crashing', () => {
        render(<MyComponent fetchData={mockFetchData} />);
    });

    it('displays loading state', async () => {
        mockFetchData.mockResolvedValueOnce([]);
        render(<MyComponent fetchData={mockFetchData} />);
        expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    it('displays error state', async () => {
        const errorMessage = 'Test Error';
        mockFetchData.mockRejectedValueOnce(new Error(errorMessage));
        render(<MyComponent fetchData={mockFetchData} />);
        await waitFor(() => screen.getByText(`Error: ${errorMessage}`));
    });

    it('displays fetched data', async () => {
        const data = ['Item 1', 'Item 2', 'Item 3'];
        mockFetchData.mockResolvedValueOnce(data);
        render(<MyComponent fetchData={mockFetchData} />);
        await waitFor(() => screen.getByText(data[0]));
        expect(screen.getByText(data[1])).toBeInTheDocument();
        expect(screen.getByText(data[2])).toBeInTheDocument();
    });

    it('calls fetchData on mount', () => {
        render(<MyComponent fetchData={mockFetchData} />);
        expect(mockFetchData).toHaveBeenCalledTimes(1);
    });
});