import os
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

warehouses = {}


@app.route('/')
def index():
    return render_template('index.html', warehouses=warehouses)


def _parse_create_form():
    name = request.form.get('name', '').strip()
    tilavuus = float(request.form.get('tilavuus', '0'))
    alku_saldo = float(request.form.get('alku_saldo', '0'))
    return name, tilavuus, alku_saldo


def _handle_create_post():
    try:
        name, tilavuus, alku_saldo = _parse_create_form()
    except ValueError:
        return render_template('create.html', error='Invalid number format')

    if not name or name in warehouses:
        error = 'Name is required' if not name else 'Name already exists'
        return render_template('create.html', error=error)

    warehouses[name] = Varasto(tilavuus, alku_saldo)
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    if request.method == 'POST':
        return _handle_create_post()
    return render_template('create.html')


def _flash_add_result(maara, available_space):
    if maara <= available_space:
        flash(f'Successfully added {maara} to warehouse.', 'success')
    else:
        added = available_space
        not_added = maara - available_space
        msg = f'Added {added}, could not add {not_added} (not enough space).'
        flash(msg, 'warning')


def _flash_remove_result(maara, removed, current_balance):
    if maara <= current_balance:
        flash(f'Successfully removed {removed} from warehouse.', 'success')
    else:
        not_removed = maara - removed
        msg = f'Removed {removed}, could not remove {not_removed} (no stock).'
        flash(msg, 'warning')


def _handle_edit_action(varasto, action, maara):
    if action == 'add':
        available_space = varasto.paljonko_mahtuu()
        varasto.lisaa_varastoon(maara)
        _flash_add_result(maara, available_space)
    elif action == 'remove':
        current_balance = varasto.saldo
        removed = varasto.ota_varastosta(maara)
        _flash_remove_result(maara, removed, current_balance)


def _handle_edit_post(name, varasto):
    try:
        maara = float(request.form.get('maara', '0'))
    except ValueError:
        return render_template(
            'edit.html', name=name, varasto=varasto, error='Invalid number'
        )

    _handle_edit_action(varasto, request.form.get('action'), maara)
    return redirect(url_for('edit_warehouse', name=name))


@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_warehouse(name):
    if name not in warehouses:
        return redirect(url_for('index'))

    varasto = warehouses[name]
    if request.method == 'POST':
        return _handle_edit_post(name, varasto)
    return render_template('edit.html', name=name, varasto=varasto)


@app.route('/delete/<name>', methods=['POST'])
def delete_warehouse(name):
    if name in warehouses:
        del warehouses[name]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
