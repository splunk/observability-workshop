from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain.tools import tool

import simplejson as json

# Postgres
import psycopg2
import psycopg2.extras

from config import Settings

class GetProductInfoArgs(BaseModel):
    skus: List[str] = Field(..., description="One or more skus to fetch product info for.")

@tool("get_products_by_sku", args_schema=GetProductInfoArgs)
def get_products_by_sku(skus: List[str]) -> List[Dict[str, Any]]:
    """Retrieves information for the specified product skus."""
    if not skus:
        return []

    # Handle case where a single string was passed accidentally
    if isinstance(skus, str):
        skus = [skus]

    connection = None
    result_products: List[Dict[str, Any]] = [] # Changed type hint

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                products_query = """
                    SELECT
                          product_id,
                          product_name,
                          product_description,
                          cost,
                          sku,
                          category,
                          active
                    FROM products
                    WHERE sku = ANY(%s)
                    ORDER BY product_id
                """
                cursor.execute(products_query, (skus,))
                product_records = cursor.fetchall()

                if not product_records:
                    return json.dumps("No products found for the provided SKUs.")

                for product_record in product_records:
                    # Create a dictionary representing the product
                    product_dict = {
                        "product_id": str(product_record['product_id']),
                        "product_name": str(product_record['product_name']),
                        "product_description": product_record['product_description'],
                        "cost": product_record['cost'],
                        "sku": product_record['sku'],
                        "category": product_record['category'],
                        "active": product_record['active']
                    }
                    result_products.append(product_dict) # Append the dictionary

                return json.dumps(result_products, use_decimal=True)

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error fetching product info {skus}: {e}")
        raise e
    finally:
        if connection is not None:
             try:
                connection.close()
             except Exception as e:
                print(f"Error closing database connection: {e}")

@tool("get_all_products")
def get_all_products() -> List[Dict[str, Any]]:
    """Retrieves information for all products."""

    connection = None
    result_products: List[Dict[str, Any]] = [] # Changed type hint

    try:
        with psycopg2.connect(Settings.DB_CONNECTION_STRING) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                products_query = """
                    SELECT
                          product_id,
                          product_name,
                          product_description,
                          cost,
                          sku,
                          category,
                          active
                    FROM products
                    ORDER BY product_id
                """
                cursor.execute(products_query)
                product_records = cursor.fetchall()

                if not product_records:
                    return json.dumps("No products found.")

                for product_record in product_records:
                    # Create a dictionary representing the product
                    product_dict = {
                        "product_id": str(product_record['product_id']),
                        "product_name": str(product_record['product_name']),
                        "product_description": product_record['product_description'],
                        "cost": product_record['cost'],
                        "sku": product_record['sku'],
                        "category": product_record['category'],
                        "active": product_record['active']
                    }
                    result_products.append(product_dict) # Append the dictionary

                return json.dumps(result_products, use_decimal=True)

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error fetching product info: {e}")
        raise e
    finally:
        if connection is not None:
             try:
                connection.close()
             except Exception as e:
                print(f"Error closing database connection: {e}")