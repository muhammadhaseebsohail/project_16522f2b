import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const TodoListWrapper = styled.div`
    padding: 20px;
    border: 1px solid #ccc;
    margin-top: 20px;
`;

const TodoItem = styled.div`
    border-bottom: 1px solid #ccc;
    padding: 10px 0;
`;

const TodoList = ({ apiUrl }) => {
    const [todos, setTodos] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const response = await axios.get(apiUrl);
                setTodos(response.data);
                setLoading(false);
            } catch (error) {
                setError(error.message);
                setLoading(false);
            }
        };
        fetchData();
    }, [apiUrl]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <TodoListWrapper>
            {todos.map((todo) => (
                <TodoItem key={todo.id}>
                    {todo.completed ? <s>{todo.title}</s> : todo.title}
                </TodoItem>
            ))}
        </TodoListWrapper>
    );
};

TodoList.propTypes = {
    apiUrl: PropTypes.string.isRequired,
};

export default TodoList;