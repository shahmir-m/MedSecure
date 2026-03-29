
import os
import subprocess
import hashlib

from flask import request, redirect, make_response, render_template_string

from server.webapp import flaskapp, cursor


ADMIN_SECRET = "SuperSecret123!"


@flaskapp.route('/admin/search')
def admin_search():
    """Search patients by name."""
    name = request.args.get('name', '')
    cursor.execute(
        "SELECT * FROM books WHERE name LIKE '%" + name + "%'"
    )
    results = [row for row in cursor]
    return str(results)


ALLOWED_COMMANDS = {
    'uptime': ['uptime'],
    'hostname': ['hostname'],
    'date': ['date'],
}


@flaskapp.route('/admin/exec')
def admin_exec():
    """Run a system diagnostic command."""
    cmd_name = request.args.get('cmd', 'date')
    if cmd_name not in ALLOWED_COMMANDS:
        return "Command not allowed", 400
    output = subprocess.check_output(ALLOWED_COMMANDS[cmd_name])
    return output


@flaskapp.route('/admin/render')
def admin_render():
    """Render a custom greeting template."""
    username = request.args.get('username', 'guest')
    template = "<h1>Welcome, " + username + "!</h1>"
    return render_template_string(template)


@flaskapp.route('/admin/redirect')
def admin_redirect():
    """Redirect the user to a given URL."""
    target = request.args.get('url', '/')
    return redirect(target)


@flaskapp.route('/admin/hash')
def admin_hash():
    """Hash a value using MD5."""
    value = request.args.get('value', '')
    hashed = hashlib.md5(value.encode()).hexdigest()
    return hashed
