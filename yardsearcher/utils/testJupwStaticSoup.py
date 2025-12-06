from jup import *

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
  x = Jup('honda civic')
  soup = BeautifulSoup(RAW_SOUP, 'lxml')
  table_rows = x.extract_inventory_table_rows(soup, x.extract_conditionals())
  x.filter_inventory_table_rows(table_rows, x.extract_conditionals())
  print('inventory_headers: ', x.inventory_headers)