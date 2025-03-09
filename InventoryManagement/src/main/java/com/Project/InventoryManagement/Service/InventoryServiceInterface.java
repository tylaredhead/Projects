package com.Project.InventoryManagement.Service;

import java.util.List;

import com.Project.InventoryManagement.Entity.Product;
import com.Project.InventoryManagement.Entity.Stock;
import com.Project.InventoryManagement.Entity.Supplier;

public interface InventoryServiceInterface {
    public Stock saveStock(Stock stock);
    public List<Stock> getAllStock();
    public Stock findById(int id);
    public List<Stock> findByRating(String rating);
    public List<Stock> findByQuantity(int quantity);
    public Stock updateRating(int id, String rating);
    public Stock updateQuantity(int id, int quantity);
    public void deleteById(int id);

    public Supplier saveSupplier(Supplier supplier);
    public List<Supplier> getAllSuppliers();
    public Supplier findBySupplierId(int id);
    public List<Supplier> findBySupplierName(String name);
    public List<Supplier> findBySupplierNo(String no);
    public List<Supplier> findBySupplierEmail(String email);
    public Supplier updateSupplierName(int id, String name);
    public Supplier updateSupplierNo(int id, String no);
    public Supplier updateSupplierEmail(int id, String email);
    public void deleteBySupplierId(int id);
    public void deleteBySupplierName(String name);

    public Product saveProduct(Product product);
    public List<Product> getAllProducts();
    public Product findByProductId(int id);
    public List<Product> findByProductName(String name);
    public List<Product> findByProductDesc(String desc);
    public List<Product> findByProductType(String type);
    public List<Product> findByPrice(float price);
    public Product updateProductName(int id, String name);
    public Product updateProductDesc(int id, String desc);
    public Product updateProductType(int id, String type);
    public Product updatePrice(int id, float price);
    public void deleteByProductId(int id);
    public void deleteByProductName(String name);
}
