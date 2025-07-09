import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { axe, toHaveNoViolations } from 'jest-axe';
import UIComponent from './UIComponent';

expect.extend(toHaveNoViolations);

describe('UIComponent', () => {
    let mockClickHandler;

    beforeEach(() => {
        mockClickHandler = jest.fn();
    });

    it('renders without crashing', () => {
        const { container } = render(<UIComponent title="Test Title" buttonLabel="Test Button" onClick={mockClickHandler} />);
        expect(container).toBeInTheDocument();
    });

    it('renders title and button label from props', () => {
        const { getByText } = render(<UIComponent title="Test Title" buttonLabel="Test Button" onClick={mockClickHandler} />);
        expect(getByText('Test Title')).toBeInTheDocument();
        expect(getByText('Test Button')).toBeInTheDocument();
    });

    it('triggers onClick handler when button is clicked', () => {
        const { getByText } = render(<UIComponent title="Test Title" buttonLabel="Test Button" onClick={mockClickHandler} />);
        fireEvent.click(getByText('Test Button'));
        expect(mockClickHandler).toHaveBeenCalled();
    });

    it('shows error message when required props are missing', () => {
        const { getByText } = render(<UIComponent />);
        expect(getByText('Error: Missing required props.')).toBeInTheDocument();
    });

    it('passes accessibility test', async () => {
        const { container } = render(<UIComponent title="Test Title" buttonLabel="Test Button" onClick={mockClickHandler} />);
        const results = await axe(container);
        expect(results).toHaveNoViolations();
    });
});