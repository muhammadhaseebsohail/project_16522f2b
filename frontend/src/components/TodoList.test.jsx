import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import '@testing-library/jest-dom/extend-expect';
import TodoList from './TodoList';

const server = setupServer(
  rest.get('/todos', (req, res, ctx) => {
    return res(ctx.json([{id: 1, title: 'Test Todo', completed: false}]))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

test('renders loading state initially', () => {
  const { getByText } = render(<TodoList apiUrl="/todos" />);
  expect(getByText('Loading...')).toBeInTheDocument();
});

test('renders todos after fetching', async () => {
  const { findByText } = render(<TodoList apiUrl="/todos" />);
  expect(await findByText('Test Todo')).toBeInTheDocument();
});

test('renders error message on fetch error', async () => {
  server.use(
    rest.get('/todos', (req, res, ctx) => {
      return res(ctx.status(500))
    })
  )

  const { findByText } = render(<TodoList apiUrl="/todos" />);
  expect(await findByText(/^Error:/)).toBeInTheDocument();
});

test('renders completed todos with strikethrough', async () => {
  server.use(
    rest.get('/todos', (req, res, ctx) => {
      return res(ctx.json([{id: 1, title: 'Test Todo', completed: true}]))
    })
  )

  const { findByText } = render(<TodoList apiUrl="/todos" />);
  expect(await findByText('Test Todo')).toHaveStyle('text-decoration: line-through;');
});

test('renders todos without strikethrough if not completed', async () => {
  server.use(
    rest.get('/todos', (req, res, ctx) => {
      return res(ctx.json([{id: 1, title: 'Test Todo', completed: false}]))
    })
  )

  const { findByText } = render(<TodoList apiUrl="/todos" />);
  expect(await findByText('Test Todo')).not.toHaveStyle('text-decoration: line-through;');
});

test('has no accessibility violations', async () => {
  const { container, findByText } = render(<TodoList apiUrl="/todos" />);
  await findByText('Test Todo');
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});