# -*- coding: utf-8 -*-
"""
GenPark Agentic Commerce A2M Bargaining Negotiator MCP Server
Exposes automated game-theoretic A2M negotiation tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkAgenticCommerceA2MBargainingNegotiator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-a2m-bargaining-negotiator", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "negotiate_a2m_deal",
                        "description": "Executes automated Rubinstein strategic bargaining and multi-item bundling negotiations between AI agents and merchant gateways.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "item_title": {"type": "string"},
                                "initial_list_price_usd": {"type": "number"},
                                "merchant_floor_price_usd": {"type": "number"},
                                "buyer_target_budget_usd": {"type": "number"},
                                "purchase_quantity": {"type": "integer"},
                                "include_warranty_bundle": {"type": "boolean"}
                            },
                            "required": ["item_title", "initial_list_price_usd", "merchant_floor_price_usd", "buyer_target_budget_usd"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "negotiate_a2m_deal":
            negotiator = GenParkAgenticCommerceA2MBargainingNegotiator()
            res = negotiator.negotiate_a2m_deal(
                item_title=args.get("item_title", "Smart Ergonomic Standing Desk"),
                initial_list_price_usd=args.get("initial_list_price_usd", 499.0),
                merchant_floor_price_usd=args.get("merchant_floor_price_usd", 380.0),
                buyer_target_budget_usd=args.get("buyer_target_budget_usd", 440.0),
                purchase_quantity=args.get("purchase_quantity", 1),
                include_warranty_bundle=args.get("include_warranty_bundle", False)
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        neg = GenParkAgenticCommerceA2MBargainingNegotiator()
        test_res = neg.negotiate_a2m_deal("Test Product", 500.0, 400.0, 450.0)
        print(f"Test Clearing Price: ${test_res['negotiated_clearing_unit_price_usd']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
