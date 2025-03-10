package com.Project.InventoryManagement.Service;

import java.util.List;

import com.Project.InventoryManagement.Entity.Product;
import com.Project.InventoryManagement.Entity.Stock;
import com.Project.InventoryManagement.Entity.Supplier;

public interface InventoryServiceInterface {
    public Stock saveStock(Stock stock); // Admin
    public List<Stock> getAllStock(); //Employee
    public Stock findById(int id); // User
    public List<Stock> findStockByProductName(String name); // User
    public List<Stock> findByRating(String rating); // User
    public List<Stock> findByQuantity(int quantity); // Employee
    public Stock updateRating(int id, String rating); // Employee
    public Stock updateQuantity(int id, int quantity); // User
    public void deleteById(int id); // Admin

    public Supplier saveSupplier(Supplier supplier); // Admin
    public List<Supplier> getAllSuppliers(); // Employee
    public Supplier findBySupplierId(int id); // Employee
    public List<Supplier> findBySupplierName(String name); // Employee
    public List<Supplier> findBySupplierNo(String no); // Employee
    public List<Supplier> findBySupplierEmail(String email); // Employee
    public Supplier updateSupplierName(int id, String name); // Admin
    public Supplier updateSupplierNo(int id, String no); // Admin
    public Supplier updateSupplierEmail(int id, String email); // Admin
    public void deleteBySupplierId(int id); // Admin
    public void deleteBySupplierName(String name); // Admin

    public Product saveProduct(Product product); // Admin
    public List<Product> getAllProducts(); // Employee
    public Product findByProductId(int id); // Employee
    public List<Product> findByProductName(String name); // User
    public List<Product> findByProductDesc(String desc); // User
    public List<Product> findByProductType(String type); // User
    public List<Product> findByPrice(float price); //User - get <> rather than discrete
    public List<Product> findProductBySupplierName(String name); // Employee
    public Product updateProductName(int id, String name); // Admin
    public Product updateProductDesc(int id, String desc); // Admin
    public Product updateProductType(int id, String type); // Admin
    public Product updatePrice(int id, float price); // Admin
    public void deleteByProductId(int id); // Admin
    public void deleteByProductName(String name); //Admin
}
