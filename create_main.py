from core.database import create_tables



if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())

