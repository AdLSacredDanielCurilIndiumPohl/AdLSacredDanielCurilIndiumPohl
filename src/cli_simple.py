#!/usr/bin/env python3
import os
import click
import json
import redis
import jwt

# Redis-Client ohne Authentifizierung
redis_client = redis.Redis(
    host='adlsacreddanielcurilindiumpohl-redis-1',
    port=6379,
    decode_responses=True
)

@click.group()
def cli():
    """Tool Management System"""
    pass

@cli.command()
@click.argument('name')
@click.argument('type')
def add(name, type):
    """Registriert ein neues Tool"""
    tool_id = f"{type}_{name}"
    
    # Generiere sicheren Token für Tool
    token = jwt.encode(
        {'tool_id': tool_id, 'type': type},
        os.environ.get('SECRET_KEY', 'dev-secret'),
        algorithm='HS256'
    )
    
    # Speichere Tool-Informationen in Redis
    tool_info = {
        'name': name,
        'type': type,
        'token': token,
        'status': 'registered'
    }
    redis_client.hset(f"tool:{tool_id}", mapping=tool_info)
    
    click.echo(f"Tool {name} ({type}) registriert mit Token: {token}")

@cli.command()
def list():
    """Listet alle registrierten Tools"""
    tool_keys = redis_client.keys('tool:*')
    if not tool_keys:
        click.echo("Keine Tools registriert")
        return

    for key in tool_keys:
        tool_info = redis_client.hgetall(key)
        click.echo(f"Tool: {tool_info['name']}")
        click.echo(f"Typ: {tool_info['type']}")
        click.echo(f"Status: {tool_info['status']}")
        click.echo("---")

@cli.command()
@click.argument('id')
def info(id):
    """Zeigt Details zu einem Tool"""
    tool_info = redis_client.hgetall(f"tool:{id}")
    if not tool_info:
        click.echo(f"Tool {id} nicht gefunden")
        return
    
    click.echo("Tool Details:")
    for key, value in tool_info.items():
        click.echo(f"{key}: {value}")

if __name__ == '__main__':
    cli()