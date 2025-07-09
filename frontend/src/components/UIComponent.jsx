import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const Container = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: #f9f9f9;
`;

const Title = styled.h1`
    font-size: 24px;
    color: #333;
    margin-bottom: 20px;
`;

const Button = styled.button`
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: #fff;
    cursor: pointer;
    &:hover {
        background-color: #0056b3;
    }
`;

function UIComponent({ title, buttonLabel, onClick }) {
    if (!title || !buttonLabel || !onClick) {
        return <p>Error: Missing required props.</p>;
    }

    return (
        <Container>
            <Title>{title}</Title>
            <Button onClick={onClick}>{buttonLabel}</Button>
        </Container>
    );
}

UIComponent.propTypes = {
    title: PropTypes.string.isRequired,
    buttonLabel: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
};

export default UIComponent;