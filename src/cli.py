#!/usr/bin/env python3
import os
import click
import json
from tool_manager import ToolManager

@click.group()
def cli():
    """Tool Management CLI"""
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def import_tools(directory):
    """Importiert Tools aus CSV/Excel-Dateien"""
    manager = ToolManager()
    manager.process_tools_directory(directory)
    manager.save_state()
    click.echo(f"Tools aus {directory} importiert")

@cli.command()
@click.argument('tool_id')
@click.option('--jwt-token', help='JWT Token für private Tools')
def get_access_url(tool_id, jwt_token):
    """Generiert eine Zugriffs-URL für ein Tool"""
    manager = ToolManager()
    manager.load_state()
    url = manager.get_tool_access_url(tool_id)
    if jwt_token and '{jwt_token}' in url:
        url = url.format(jwt_token=jwt_token)
    click.echo(url)

@cli.command()
def list_tools():
    """Listet alle verfügbaren Tools"""
    manager = ToolManager()
    manager.load_state()
    for config in manager.tools_config.values():
        for tool in config:
            click.echo(f"{tool['name']} ({tool['type']}) - {tool['description']}")

@cli.command()
@click.argument('tool_name')
def deploy(tool_name):
    """Deployed ein spezifisches Tool"""
    manager = ToolManager()
    manager.load_state()
    
    # Suche Tool in der Konfiguration
    tool_config = None
    for config in manager.tools_config.values():
        for tool in config:
            if tool['name'] == tool_name:
                tool_config = tool
                break
        if tool_config:
            break
    
    if not tool_config:
        click.echo(f"Tool {tool_name} nicht gefunden")
        return
    
    tool_id = manager.deploy_tool(tool_config)
    manager.save_state()
    click.echo(f"Tool {tool_name} deployed mit ID {tool_id}")

if __name__ == '__main__':
    cli()