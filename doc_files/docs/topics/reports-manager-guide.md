---
description: Viewing sales reports is an important aspect of managing Gold Fin Apparel, and the reports manager provides valuable insights into customer orders and product performance.
---
# Managing Sales Reports

Viewing sales reports is an important aspect of managing Gold Fin Apparel, and the reports manager provides valuable insights into customer orders and product performance. You can view reports that show unique orders and quantities by customer and date, and every unique item ordered along with its attributes and the total quantity sold for each item. This can be used to make informed decisions about inventory management, marketing strategies, and overall business performance.

## Accessing Sales Reports

!!! note "Prerequisites"

    Viewing sales reports requires that you have the most recent project repository with the latest updates. You can clone the project repository from GitHub at [Gold_Fin_Apparel](https://github.com/goldfinger-group/Gold_Fin_Apparel/tree/dev).

    You will also need Zowe Explorer v3.4.2 installed for Visual Studio Code to access the mainframe environment and view the sales reports. You can install the Zowe Explorer extension from the Visual Studio Code marketplace.

    For configuring Zowe Explorer to connect to your mainframe environment, see more at [Zowe Explorer Documentation](https://docs.zowe.org/stable/user-guide/ze-install-configuring-ze/).


1. Open Visual Studio Code and navigate to the Zowe Explorer panel.

1. Right Click the `zosmf` file and select Create New Data Set.

    1. Name the Data Set: `<USERID>.PROJECT.REPORTS`

    1. Select Partitioned Data Set Default

    1. Allocate New Data Set

1. Right Click the newly created Data Set and select Create New Member. You will need to create two members to store the sales reports.

    1. Name member one: `QUERYJCL`

    1. Name member two: `SQL1`

1. Navigate to jobs/queryjcl, in the Gold Fin Apparel project repository, and copy the contents of `QUERYJCL.jcl` into the `QUERYJCL` member you just created.

!!! note "Note"

    Update the path in the `JCL` file to point to the `SQL` file you just created. The path should be: `<USERID>.PROJECT.REPORTS(SQL1)`.

1. Navigate to jobs/sql1, in the Gold Fin Apparel project repository, and copy the contents of `SQL1` into the `SQL1` member you just created.

1. Save both members and submit the `QUERYJCL` job to run the SQL query and generate the sales reports.

## Viewing the Sales Reports

After a job has successfully submitted, you can view the output in the Zowe Explorer panel under the Jobs section. Look for the job you just submitted and click on it to see the details. The output will include the results of the SQL query, which will show the sales reports based on the criteria defined in the `SQL1` file.

The sales reports will include the following information:

- Unique orders and quantities by customer, showing customer ID, product ID, design ID, and total quantity.

- Sales data by date, showing date, product ID, design ID, and total quantity.

- Every unique item ordered along with its attributes (size, style, material, color) and the total quantity sold for each item.
