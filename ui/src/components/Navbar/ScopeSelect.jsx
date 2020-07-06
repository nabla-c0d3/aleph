import React from 'react';
import c from 'classnames';
import { Button, MenuItem } from '@blueprintjs/core';
import { Select } from '@blueprintjs/select';

import './ScopeSelect.scss';

class ScopeSelect extends React.Component {
  renderItem = (scope, { index }) => (
    <MenuItem
      key={index}
      onClick={() => this.props.onChangeScope(scope)}
      text={scope.listItem}
    />
  )

  render() {
    const { scopes, activeScope } = this.props;
    const multipleScopes = scopes.length > 1;
    return (
      <Select
        filterable={false}
        items={scopes}
        itemRenderer={this.renderItem}
        popoverProps={{
          minimal: true,
          popoverClassName: 'ScopeSelect__popover',
          usePortal: true,
        }}
        disabled={!multipleScopes}
        className="ScopeSelect"
      >
        <Button
          className={c('ScopeSelect__scope-button', { unclickable: !multipleScopes })}
          text={activeScope.listItem}
          rightIcon={multipleScopes ? 'caret-down' : null}
        />
      </Select>
    );
  }
}

export default ScopeSelect;
