package com.Project.InventoryManagement.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Supplier {
    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)
    @Column(name="supplierId", unique=true)
    private int supplierId;
    @Column(name="supplierName")
    private String supplierName;
    @Column(name="supplierNo")
    private String supplierNo;
    @Column(name="supplierEmail")
    private String supplierEmail;

    public Supplier(){}

    public Supplier(String supplierName, String supplierNo, String supplierEmail){
        this.supplierName = supplierName;
        this.supplierNo = supplierNo;
        this.supplierEmail = supplierEmail;
    }

    public int getSupplierId(){
        return supplierId;
    }

    public void setSupplierId(int id){
        this.supplierId = id;
    }

    public String getSupplierName(){
        return supplierName;
    }

    public void setSupplierName(String supplierName){
        this.supplierName = supplierName;
    }

    public String getSupplierNo(){
        return supplierNo;
    }

    public void setSupplierNo(String no){
        this.supplierNo = no;
    }

    public String getSupplierEmail(){
        return supplierEmail;
    }

    public void setSupplierEmail(String email){
        this.supplierEmail = email;
    }

    @Override
    public String toString(){
        return "Supplier{" + supplierId + ", " + supplierName + ", " + supplierNo + ", " + supplierEmail + "}";
    }
}

