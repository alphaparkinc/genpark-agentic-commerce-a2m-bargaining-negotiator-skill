# -*- coding: utf-8 -*-
"""
Example usage of GenParkAgenticCommerceA2MBargainingNegotiator
Demonstrates automated multi-round A2M strategic negotiation.
"""

from client import GenParkAgenticCommerceA2MBargainingNegotiator

def main():
    negotiator = GenParkAgenticCommerceA2MBargainingNegotiator(buyer_discount_factor=0.94, merchant_discount_factor=0.86)

    cases = [
        {
            "name": "Case 1: Single Unit High-End Smartphone Gimbal",
            "item": "AI Auto-Tracking 3-Axis Gimbal Stabilizer",
            "list": 299.00, "floor": 220.00, "budget": 260.00, "qty": 1, "warranty": True
        },
        {
            "name": "Case 2: Bulk Purchase Corporate Ergonomic Chairs (5 Units)",
            "item": "Mesh Ergonomic Task Chair Pro",
            "list": 380.00, "floor": 270.00, "budget": 320.00, "qty": 5, "warranty": False
        }
    ]

    print("================================================================")
    print("GenPark Agentic Commerce A2M Negotiator - Live Deals")
    print("================================================================\n")

    for c in cases:
        res = negotiator.negotiate_a2m_deal(
            item_title=c["item"],
            initial_list_price_usd=c["list"],
            merchant_floor_price_usd=c["floor"],
            buyer_target_budget_usd=c["budget"],
            purchase_quantity=c["qty"],
            include_warranty_bundle=c["warranty"]
        )
        print(f"[{c['name']}]")
        print(f"  Item                  : {res['item_title']} (Qty: {res['purchase_quantity']})")
        print(f"  Original List Total   : ${c['list'] * c['qty']:,.2f}")
        print(f"  Settlement Total      : ${res['total_order_settlement_usd']:,.2f} (${res['negotiated_clearing_unit_price_usd']}/unit)")
        print(f"  Total Net Savings     : ${res['total_savings_achieved_usd']:,.2f} (-{res['discount_percentage']}%)")
        print(f"  Rounds to Agreement   : {res['negotiation_rounds_executed']} rounds")
        print(f"  Nash Equilibrium Effic: {res['nash_equilibrium_efficiency_pct']}% [{res['deal_verdict']}]\n")

if __name__ == "__main__":
    main()
