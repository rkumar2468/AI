import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    mini = 0
    ret = None
    for x in shops:
        temp = x.getPriceOfOrder(orderList)
        #print temp
        if mini == 0:
            mini = temp
            ret = x
        elif temp < mini:
            mini = temp
            ret = x
    return ret

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  #shopSmart(orders, shops)
  print "For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName()
  orders = [('apples',3.0)]
  print "For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName()