"""from jup import *

if __name__ == '__main__':
  RAW_SOUP = '''
  <table class="table resultsTable parts-table" id="cars-table">
<tr>
<th>Year</th>
<th>Make</th>
<th>Model</th>
<th>Stock#</th>
<th>Vehicle Row</th>
<th>Date Set in Yard</th>
</tr>
<tr>
<td>2003</td>
<td>MITSUBISHI</td>
<td>ECLIPSE</td>
<td>STK069917</td>
<td>18</td>
<td>11.03.25</td>
</tr>
<tr>
<td>2003</td>
<td>MITSUBISHI</td>
<td>ECLIPSE</td>
<td>STK070227</td>
<td>86</td>
<td>11.20.25</td>
</tr>
</table>

  '''
  # x = Jup('honda civic')
  # soup = BeautifulSoup(RAW_SOUP, 'lxml')
  # table_rows = x.extract_inventory_table_rows(soup, x.extract_conditionals())
  # x.filter_inventory_table_rows(table_rows, x.extract_conditionals())
  # print('inventory_headers: ', x.inventory_headers)

  # # Testing satisfies conditionals by checking results when no year or range is present
  # x = Jup('honda accord')
  # soup = BeautifulSoup(RAW_SOUP, 'lxml')
  # table_rows = x.extract_inventory_table_rows(soup, x.extract_conditionals())
  # x.filter_inventory_table_rows(table_rows, x.extract_conditionals())
  # print('\nresults :', x.results)

  # # Testing satisfies conditionals when expected year is present
  # x = Jup('2003 mitsubishi eclipse')
  # soup = BeautifulSoup(RAW_SOUP, 'lxml')
  # table_rows = x.extract_inventory_table_rows(soup, x.extract_conditionals())
  # x.filter_inventory_table_rows(table_rows, x.extract_conditionals())
  # print('\nresults :', x.results)
  # # results : [('2003', 'mitsubishi', 'eclipse', 'stk069917', '18', '11.03.25'), ('2003', 'mitsubishi', 'eclipse', 'stk070227', '86', '11.20.25')]

#   # Testing satisfies conditionals when unexpected year is present
#   x = Jup('2012 mitsubishi eclipse')
#   soup = BeautifulSoup(RAW_SOUP, 'lxml')
#   table_rows = x.extract_inventory_table_rows(soup, x.extract_conditionals())
#   x.filter_inventory_table_rows(table_rows, x.extract_conditionals())
#   print('\nresults :', x.results)
# #results : [] As expected

#  # Testing satisfies conditionals when year range is present
#   x = Jup('03-12 mitsubishi eclipse')
#   soup = BeautifulSoup(RAW_SOUP, 'lxml')
#   table_rows = x.extract_inventory_table_rows(soup, x.extract_conditionals())
#   x.filter_inventory_table_rows(table_rows, x.extract_conditionals())
#   print('\nresults :', x.results)
# #results : [('2003', 'mitsubishi', 'eclipse', 'stk069917', '18', '11.03.25'), ('2003', 'mitsubishi', 'eclipse', 'stk070227', '86', '11.20.25')]


# # Testing an actual search with year range present:
# x= Jup('2000-2006 honda civic')
# x.handle_queries()
# print('\nresults :', x.results)

# Testing an actual search with year range present:
x= Jup('2000-2008 ford mustang')
x.handle_queries()
print('\n data dict :', x.data_as_dict())"""