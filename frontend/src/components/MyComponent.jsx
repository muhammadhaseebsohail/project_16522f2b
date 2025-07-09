import React from 'react';
import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import styles from './MyComponent.module.css';

const MyComponent = ({ fetchData }) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIsLoading(true);
    fetchData()
      .then(response => setData(response))
      .catch(error => setError(error))
      .finally(() => setIsLoading(false));
  }, [fetchData]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div className={styles.container}>
      {data && data.map((item, index) => (
        <div key={index} className={styles.item}>
          {item}
        </div>
      ))}
    </div>
  );
};

MyComponent.propTypes = {
  fetchData: PropTypes.func.isRequired,
};

export default MyComponent;

// Testing code

import React from 'react';
import { shallow } from 'enzyme';
import MyComponent from './MyComponent';

describe('MyComponent', () => {
  let wrapper;
  const mockFetchData = jest.fn();

  beforeEach(() => {
    mockFetchData.mockClear();
    wrapper = shallow(<MyComponent fetchData={mockFetchData} />);
  });

  it('should render correctly', () => {
    expect(wrapper).toMatchSnapshot();
  });

  it('should display loading state', () => {
    wrapper.setState({ isLoading: true });
    expect(wrapper.contains(<div>Loading...</div>)).toBe(true);
  });

  it('should display error state', () => {
    const error = { message: 'Test Error' };
    wrapper.setState({ error });
    expect(wrapper.contains(<div>Error: {error.message}</div>)).toBe(true);
  });

  it('should call fetchData on mount', () => {
    expect(mockFetchData).toHaveBeenCalledTimes(1);
  });
});