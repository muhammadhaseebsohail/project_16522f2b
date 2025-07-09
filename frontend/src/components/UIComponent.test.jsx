import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import '@testing-library/jest-dom/extend-expect';
import UIComponent from './UIComponent';

const server = setupServer(
  rest.get('/mocked-endpoint', (req, res, ctx) => {
    return res(ctx.json(['item1', 'item2', 'item3']))
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('checks if component is rendered', () => {
  render(<UIComponent url="/mocked-endpoint" />);
});

test('checks if loading state is rendered', () => {
  server.use(
    rest.get('/mocked-endpoint', (req, res, ctx) => {
      return res(ctx.delay(1500), ctx.json(['item1', 'item2', 'item3']));
    })
  );
  
  render(<UIComponent url="/mocked-endpoint" />);
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});

test('checks if error state is rendered', async () => {
  server.use(
    rest.get('/mocked-endpoint', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );
  
  render(<UIComponent url="/mocked-endpoint" />);
  await waitFor(() => {
    expect(screen.getByText(/An error occurred:/i)).toBeInTheDocument();
  });
});

test('checks if data is rendered', async () => {
  render(<UIComponent url="/mocked-endpoint" />);
  await waitFor(() => {
    expect(screen.getByText('item1')).toBeInTheDocument();
    expect(screen.getByText('item2')).toBeInTheDocument();
    expect(screen.getByText('item3')).toBeInTheDocument();
  });
});

test('checks prop types', () => {
  console.error = jest.fn();
  render(<UIComponent />);
  expect(console.error).toHaveBeenCalled();
});

test('checks accessibility', async () => {
  const { container } = render(<UIComponent url="/mocked-endpoint" />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});