package com.sfx.JavaLambda;


public class Order {
 	private String phoneType;
	private int    quantity = 1;
    private String customerType;
    private double price;
	private String transaction;
    private String approval;

    public void setOrder(String phoneType, int quantity, String customerType, double price, String transaction, String approval) {
		this.phoneType = phoneType;
		this.quantity = quantity;
        this.customerType = customerType;
        this.price=price;
		this.transaction = transaction;
        this.approval = approval;
	}
    
    /**
     * @return String return the phoneType
     */
    public String getPhoneType() {
        return phoneType;
    }

    /**
     * @param phoneType the phoneType to set
     */
    public void setPhoneType(String phoneType) {
        this.phoneType = phoneType;
    }

    /**
     * @return String return the Quantity
     */
    public int getQuantity() {
        return quantity;
    }

    /**
     * @param Quantity the Quantity to set
     */
    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    /**
     * @return String return the CustomerType
     */
    public String getCustomerType() {
        return customerType;
    }

    /**
     * @param CustomerType the CustomerType to set
     */
    public void setCustomerType(String customerType) {
        this.customerType = customerType;
    }

    /**
     * @return String return the Transaction
     */
    public String getTransaction() {
        return transaction;
    }

    /**
     * @param Transaction the Transaction to set
     */
    public void setTransaction(String transaction) {
        this.transaction = transaction;
    }

    /**
     * @return Float return the price
     */
    public double getPrice() {
        return price;
    }

    /**
     * @param price the price to set
     */
    public void setPrice(double price) {
        this.price = price;
    }

 
    /**
     * @return String return the approval
     */
    public String getApproval() {
        return approval;
    }

    /**
     * @param approval the Approval to set
     */
    public void setApproval(String approval) {
        this.approval = approval;
    }   

}